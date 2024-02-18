from flask import request
from sqlalchemy import desc

from application.common import toolbox
from application.models.actions import Actions
from application.models.games import Games


@staticmethod
def get_all_games(add_server_status=False):
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 1000000)

    games_dict = Games.to_collection_dict(
        Games.query, page, per_page, "game.get_all_games"
    )

    # For a server with 2-5 games, this for loop is not a problem.  The author knows that
    # a join is more optimal for database items.
    game_items = games_dict["items"]

    # Mixin other items, like actions
    for game in game_items:
        actions_qry = Actions.query.filter_by(game_id=game["game_id"]).order_by(
            desc(Actions.timestamp)
        )

        # This wil get the first per_page items (10 by default)
        actions_dict = Actions.to_collection_dict(
            actions_qry, page, per_page, "game.get_all_games"
        )
        game["actions"] = actions_dict["items"]

    if add_server_status:
        for game in game_items:
            # From .py file not db.
            game_obj = toolbox._get_supported_game_object(game["game_name"])
            game["game_exe"] = game_obj._game_executable
            has_pid = True if game["game_pid"] != "null" else False
            is_exe_found = toolbox._get_proc_by_name(game_obj._game_executable)
            game["game_status"] = (
                "Running" if is_exe_found and has_pid else "Not Running"
            )

    return games_dict


@staticmethod
def get_game_by_name(game_name):
    game_query = Games.query.filter_by(game_name=game_name)
    game_dict = Games.to_collection_dict(
        game_query, 1, 1, "game.get_game_by_name", game_name=game_name
    )

    if len(game_dict["items"]) == 0:
        return game_dict

    game_item = game_dict["items"][0]
    actions_qry = Actions.query.filter_by(game_id=game_item["game_id"]).order_by(
        desc(Actions.timestamp)
    )

    # This wil get the first per_page items (10 by default)
    actions_dict = Actions.to_collection_dict(
        actions_qry, 1, 10, "game.get_game_by_name", game_name=game_name
    )
    game_dict["actions"] = actions_dict["items"]

    return game_dict


@staticmethod
def get_games_schema():
    valid_cols = []

    for column in Games.__table__.columns:
        valid_cols.append(column.name)

    return valid_cols


@staticmethod
def get_game_server_status(game_name: str) -> str:
    response = {}
    status = "Error"  # Assume error unless otherwise proved.

    response.update({"status": status})

    game_obj = Games.query.filter_by(game_name=game_name).first()

    if game_obj is None:
        return response

    game_data = toolbox._get_supported_game_object(game_name)
    exe_name = game_data._game_executable

    game_pid = game_obj.game_pid
    is_exe_found = True if toolbox._get_proc_by_name(exe_name) is not None else False
    is_valid_pid = True if game_pid is not None else False
    is_running = is_exe_found and is_valid_pid
    status = "Running" if is_running else "Not Running"

    response.update(
        {
            "is_exe_found": is_exe_found,
            "is_valid_pid": is_valid_pid,
            "is_running": is_running,
            "status": status,
        }
    )

    return response
