from flask import Blueprint, request, jsonify

from application.common import logger
from application.common.decorators import authorization_required
from application.common.exceptions import InvalidUsage
from application.managers.steam_manager import SteamManager

steam = Blueprint("steam", __name__, url_prefix="/v1")


###############################################################################
###############################################################################
# Steam Manager Endpoints
###############################################################################
###############################################################################


@steam.route("/steam/app/install", methods=["POST"])
@authorization_required
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

    try:
        steam_mgr = SteamManager(payload["steam_install_path"])
    except Exception as error:
        logger.critical(error)
        return "Error", 500

    install_thread = steam_mgr.install_steam_app(
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

    logger.info("Steam Application has been installed")

    return jsonify(
        {
            "thread_name": install_thread.name,
            "thread_ident": install_thread.native_id,
            "activity": "install",
        }
    )


@steam.route("/steam/app/update", methods=["POST"])
@authorization_required
def steam_app_update():
    logger.info("Updating Steam Application")

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

    try:
        steam_mgr = SteamManager(payload["steam_install_path"])
    except Exception as error:
        logger.critical(error)
        return "Error", 500

    update_thread = steam_mgr.update_steam_app(
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

    logger.info("Steam Application has been updated")

    return jsonify(
        {
            "thread_name": update_thread.name,
            "thread_ident": update_thread.native_id,
            "activity": "install",
        }
    )


# TODO - Implement this functionality.
@steam.route("/steam/app/remove", methods=["POST"])
@authorization_required
def steam_app_remove():
    logger.info("Remote uninstalls of game servers Not Yet Implemented")
    return "Success"
