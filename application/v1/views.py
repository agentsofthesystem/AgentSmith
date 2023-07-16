import os

from flask import Blueprint, jsonify, request
from application.common import logger
from application.common.exceptions import InvalidUsage
from application.v1.source import manager

application = Blueprint("application", __name__, url_prefix="/v1")


## Application Endpoints
@application.route("/app/install", methods=["POST"])
def install():
    logger.info("Installing Application")

    payload = request.json

    required_data = [
        "steam_install_path",
        "steam_id",
        "install_dir",
        "user",
        "password",
    ]

    if required_data != list(payload.keys()):
        message = "Error: Missing Required Data"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    steam_mgr = manager.SteamManager(payload["steam_install_path"])

    steam_mgr.install_steam_app(
        payload["steam_id"],
        payload["install_dir"],
        payload["user"],
        payload["password"],
    )

    logger.info("Application has been installed")
    return "Success"


@application.route("/app/remove", methods=["POST"])
def remove():
    logger.info("Application has been removed")
    return "Success"


@application.route("/app/update", methods=["POST"])
def update():
    logger.info("Application has been updated")
    return "Success"


@application.route("/app/start", methods=["POST"])
def start():
    logger.info("Starting Application")

    input_args = None
    payload = request.json

    required_data = [
        "app_name",
        "app_path",
    ]

    if not set(required_data).issubset(set(payload.keys())):
        message = "Error: Missing Required Data"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    if "input_args" in payload.keys():
        input_args = payload["input_args"]

    game_manager = manager.GameManager(payload["app_name"], payload["app_path"])

    try:
        game_manager.start_game(input_args)
    except Exception:
        message = "Unable to start application."
        logger.error(message)
        raise InvalidUsage(message, status_code=500)

    logger.info(f"Application Started, {payload['app_name']}")

    return "Success"


@application.route("/app/stop", methods=["POST"])
def stop():
    logger.info("Stopping Application...")

    payload = request.json

    required_data = [
        "app_name",
    ]

    if not set(required_data).issubset(set(payload.keys())):
        message = "Error: Missing Required Data"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    game_manager = manager.GameManager(payload["app_name"], "")

    try:
        is_stopped = game_manager.stop_game(payload["app_name"])
    except Exception:
        message = "Unable to start application."
        logger.error(message)
        raise InvalidUsage(message, status_code=500)

    logger.info(f"Application Stopped, {payload['app_name']}")

    output = {"IS_STOPPED": "TRUE" if is_stopped else "FALSE"}

    return jsonify(output)


@application.route("/app/restart", methods=["POST"])
def restart():
    logger.info("Application has Restarted")
    return "Success"


@application.route("/app/alive", methods=["GET"])
def is_application_alive():
    logger.info("Checking on application heartbeat.")
    app_name = request.args.get("app_name", None, str)

    if app_name is None:
        raise InvalidUsage(
            "Error: Missing Input Argument, 'app_name'.", status_code=400
        )

    game_manager = manager.GameManager(app_name, "")

    alive = "ALIVE" if game_manager.game_is_found(app_name) else "NOT_FOUND"

    alive = {"HEART_BEAT": alive}

    return jsonify(alive)


@application.route("/app/status", methods=["GET"])
def application_status():
    logger.info("Checking on application status information.")
    app_name = request.args.get("app_name", None, str)

    if app_name is None:
        raise InvalidUsage(
            "Error: Missing Input Argument, 'app_name'.", status_code=400
        )

    game_manager = manager.GameManager(app_name, "")

    process_info = game_manager.game_status(app_name)

    if process_info:
        return jsonify(process_info)
    else:
        return jsonify("NOT_RUNNING")


## Key/Access Related Endpoints


@application.route("/key/generate", methods=["POST"])
def key_generate():
    logger.info("Application Generating Control Key")
    return "Success"


@application.route("/key/verify", methods=["POST"])
def key_verify():
    logger.info("Application Key Verification - Checking....")
    return "Success"
