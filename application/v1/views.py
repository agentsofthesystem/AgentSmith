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

    result = steam_mgr.install_steam_app(
        payload["steam_id"],
        payload["install_dir"],
        payload["user"],
        payload["password"],
    )

    if result.returncode > 0:
        message = (
            f"Warning: Installation returned non-zero exit code: {result.returncode}"
        )
        logger.error(message)

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
    logger.info("Application has Stopped")
    return "Success"


@application.route("/app/restart", methods=["POST"])
def restart():
    logger.info("Application has Restarted")
    return "Success"


@application.route("/app/status", methods=["GET"])
def application_status():
    logger.info("Checking on application.")
    app_name = request.args.get("app_name", None, str)

    if app_name is None:
        raise InvalidUsage(
            "Error: Missing Input Argument, 'app_name'.", status_code=400
        )

    game_manager = manager.GameManager(app_name, "")

    is_running = game_manager.check_game(app_name)

    status = "ALIVE" if is_running else "NOT_RUNNING"

    status = {"status": status}

    return jsonify(status)


## Key/Access Related Endpoints


@application.route("/key/generate", methods=["POST"])
def key_generate():
    logger.info("Application Generating Control Key")
    return "Success"


@application.route("/key/verify", methods=["POST"])
def key_verify():
    logger.info("Application Key Verification - Checking....")
    return "Success"
