from flask import Blueprint, jsonify

from application.common import logger
from application.common.decorators import authorization_required
from application.managers.steam_manager import SteamUpdateManager
from application.api.controllers import architect as architect_controller
from application.api.controllers import games as games_controller

architect = Blueprint("architect", __name__, url_prefix="/v1/architect")


# Unprotected version...
@architect.route("/health", methods=["GET"])
def health():
    logger.info("App is alive!")
    return jsonify("Alive")


@architect.route("/health/secure", methods=["GET"])
@authorization_required
def health_secure():
    logger.info("App is alive!")
    return jsonify("Alive")


@architect.route("/agent/info", methods=["GET"])
@authorization_required
def agent_info():
    steam_mgr = SteamUpdateManager()
    info = {}

    platform_dict = architect_controller.get_platform_info()

    games = games_controller.get_all_games(add_server_status=True)
    games = games["items"]

    # TODO - Tech Debt: Update agent info page to get this info over websocket. Works for now
    # but does not scale.
    for game in games:
        game_steam_id = game["game_steam_id"]
        try:
            update_dict = steam_mgr.is_update_required(
                game["game_steam_build_id"],
                game["game_steam_build_branch"],
                game_steam_id,
            )
            game["update_required"] = update_dict["is_required"]
            game["update_required_error"] = update_dict["error"]
        except Exception:
            game["update_required"] = "ERROR"
            logger.error(
                f"Unable to retrieve game info for game_steam_id: {game_steam_id}",
                exc_info=True,
            )

    info: dict = platform_dict
    info.update({"games": games})

    return jsonify(info)
