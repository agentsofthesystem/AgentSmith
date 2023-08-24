import os

from flask import request

from application.api.v1.source.models.games import Games


@staticmethod
def get_resources_dir() -> str:
    current_file = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_file)
    resources_folder = os.path.join(current_folder, "resources")
    return resources_folder


def get_games_schema():
    valid_cols = []

    for column in Games.__table__.columns:
        valid_cols.append(column.name)

    return valid_cols


def get_all_games():
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", 10, type=int), 10000
    )  # TODO Replace update limit

    all_games_qry = Games.query

    data = Games.to_collection_dict(all_games_qry, page, per_page, "game.get_all_games")

    return data
