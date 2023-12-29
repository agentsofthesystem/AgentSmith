from flask import Blueprint, jsonify

from application.common import logger
from application.common.decorators import authorization_required
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
    info = {}

    platform_dict = architect_controller.get_platform_info()

    games = games_controller.get_all_games(add_server_status=True)
    games = games["items"]

    info: dict = platform_dict
    info.update({"games": games})

    return jsonify(info)
