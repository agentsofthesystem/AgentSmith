from datetime import datetime
from flask import Blueprint, request, jsonify

from application.common import logger
from application.common.constants import GameActionTypes
from application.common.decorators import authorization_required
from application.common.exceptions import InvalidUsage
from application.extensions import DATABASE
from application.managers.steam_manager import SteamManager
from application.models.actions import Actions
from application.models.games import Games

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

    game_obj = Games.query.filter_by(
        game_steam_id=steam_id, game_install_dir=payload["install_dir"]
    ).first()

    try:
        new_action = Actions()
        new_action.type = GameActionTypes.INSTALLING.value
        new_action.game_id = game_obj.game_id
        new_action.result = install_thread.native_id
        DATABASE.session.add(new_action)
        DATABASE.session.commit()
    except Exception:
        message = "SteamManager: install_steam_app -> Error: Failed to update database."
        logger.critical(message)
        raise InvalidUsage(message, status_code=500)

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

    game_qry = Games.query.filter_by(
        game_steam_id=steam_id, game_install_dir=payload["install_dir"]
    )
    game_obj = game_qry.first()

    try:
        new_action = Actions()
        new_action.type = GameActionTypes.UPDATING.value
        new_action.game_id = game_obj.game_id
        new_action.result = update_thread.native_id
        game_obj.game_last_update = datetime.now()
        DATABASE.session.add(new_action)
        DATABASE.session.commit()
    except Exception:
        message = "SteamManager: install_steam_app -> Error: Failed to update database."
        logger.critical(message)
        raise InvalidUsage(message, status_code=500)

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


# TODO - Deprecate this - Was implemented in game_base. No longer needed.
@steam.route("/steam/app/remove", methods=["POST"])
@authorization_required
def steam_app_remove():
    logger.info("Remote uninstalls of game servers Not Yet Implemented")
    return "Success"


@steam.route("/steam/app/build/id", methods=["POST"])
@authorization_required
def steam_app_get_build_id():
    logger.info("Getting Steam Application Manifest Build ID")

    payload = request.json

    required_data = ["steam_install_path", "game_install_path", "steam_id"]

    if not set(required_data).issubset(set(list(payload.keys()))):
        message = "Error: Missing Required Data"
        logger.error(message)
        logger.info(payload.keys())
        raise InvalidUsage(message, status_code=400)

    steam_id = payload["steam_id"]
    steam_install_path = payload["steam_install_path"]
    game_install_path = payload["game_install_path"]

    steam_mgr = SteamManager(steam_install_path, force_steam_install=False)
    app_info = steam_mgr.get_build_id_from_app_manifest(game_install_path, steam_id)

    return jsonify(app_info)
