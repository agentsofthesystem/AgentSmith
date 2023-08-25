from flask import Blueprint, request
from application.common import logger
from application.common.exceptions import InvalidUsage
from application.source.steam_manager import SteamManager

steam = Blueprint("steam", __name__, url_prefix="/v1")


###############################################################################
###############################################################################
## Steam Manager Endpoints
###############################################################################
###############################################################################


@steam.route("/steam/app/install", methods=["POST"])
def steam_app_install():
    logger.info("Installing Steam Application")

    payload = request.json

    required_data = [
        "steam_install_path",
        "steam_id",
        "install_dir",
        "user",
        "password",
    ]

    if not set(required_data).issubset(set(list(payload.keys()))):
        message = "Error: Missing Required Data"
        logger.error(message)
        logger.info(payload.keys())
        raise InvalidUsage(message, status_code=400)

    steam_id = payload["steam_id"]
    steam_mgr = SteamManager(payload["steam_install_path"])

    steam_mgr.install_steam_app(
        steam_id,
        payload["install_dir"],
        payload["user"],
        payload["password"],
    )

    payload.pop("steam_install_path")
    payload.pop("steam_id")
    payload.pop("install_dir")
    payload.pop("user")
    payload.pop("password")

    # Check if args were included.
    if len(payload.keys()) > 0:
        steam_mgr.save_game_arguments(steam_id, payload)

    logger.info("Steam Application has been installed")

    return "Success"


@steam.route("/steam/app/remove", methods=["POST"])
def steam_app_remove():
    logger.info("Steam Application has been removed")
    return "Success"


@steam.route("/steam/app/update", methods=["POST"])
def steam_app_update():
    logger.info("Steam Application has been updated")
    return "Success"
