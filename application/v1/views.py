import os

from flask import Blueprint, jsonify, request
from application.common import logger
from application.common.exceptions import InvalidUsage
from application.v1.source.executable_manager import GenericExecutableManager
from application.v1.source.steam_manager import SteamManager

application = Blueprint("application", __name__, url_prefix="/v1")


###############################################################################
###############################################################################
## Steam Manager Endpoints
###############################################################################
###############################################################################


@application.route("/steam/app/install", methods=["POST"])
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

    if required_data != list(payload.keys()):
        message = "Error: Missing Required Data"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    steam_mgr = SteamManager(payload["steam_install_path"])

    steam_mgr.install_steam_app(
        payload["steam_id"],
        payload["install_dir"],
        payload["user"],
        payload["password"],
    )

    logger.info("Steam Application has been installed")
    return "Success"


@application.route("/steam/app/remove", methods=["POST"])
def steam_app_remove():
    logger.info("Steam Application has been removed")
    return "Success"


@application.route("/steam/app/update", methods=["POST"])
def steam_app_update():
    logger.info("Steam Application has been updated")
    return "Success"


###############################################################################
###############################################################################
### Generic Executable
###############################################################################
###############################################################################


@application.route("/exe/launch", methods=["POST"])
def launch_executable():
    logger.info("Starting Generic Executable")

    input_args = None
    payload = request.json

    required_data = [
        "exe_name",
        "exe_path",
    ]

    if not set(required_data).issubset(set(payload.keys())):
        message = "Error: Missing Required Data"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    if "input_args" in payload.keys():
        input_args = payload["input_args"]

    exe_manager = GenericExecutableManager(payload["exe_name"], payload["exe_path"])

    try:
        exe_manager.launch_executable(input_args)
    except Exception:
        message = "Unable to launch executable."
        logger.error(message)
        raise InvalidUsage(message, status_code=500)

    logger.info(f"Executable Started, {payload['exe_name']}")

    return "Success"


@application.route("/exe/kill", methods=["POST"])
def kill_executable():
    logger.info("Killing Executable...")

    payload = request.json

    required_data = [
        "exe_name",
    ]

    if not set(required_data).issubset(set(payload.keys())):
        message = "Error: Missing Required Data"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    exe_manager = GenericExecutableManager(payload["exe_name"], "")

    try:
        is_stopped = exe_manager.kill_executable(payload["exe_name"])
    except Exception:
        message = "Unable to start application."
        logger.error(message)
        raise InvalidUsage(message, status_code=500)

    logger.info(f"Executable Stopped, {payload['exe_name']}")

    output = {"IS_STOPPED": "TRUE" if is_stopped else "FALSE"}

    return jsonify(output)


@application.route("/exe/restart", methods=["POST"])
def restart():
    logger.info("Executable has Restarted")
    return "Success"


@application.route("/exe/status", methods=["GET"])
def application_status():
    logger.info("Checking on application status information.")
    exe_name = request.args.get("exe_name", None, str)

    if exe_name is None:
        raise InvalidUsage(
            "Error: Missing Input Argument, 'exe_name'.", status_code=400
        )

    exe_manager = GenericExecutableManager(exe_name, "")

    process_info = exe_manager.executable_status(exe_name)

    if process_info:
        return jsonify(process_info)
    else:
        return jsonify("NOT_RUNNING")


@application.route("/exe/alive", methods=["GET"])
def is_application_alive():
    logger.info("Checking on application heartbeat.")
    exe_name = request.args.get("exe_name", None, str)

    if exe_name is None:
        raise InvalidUsage(
            "Error: Missing Input Argument, 'exe_name'.", status_code=400
        )

    exe_manager = GenericExecutableManager(exe_name, "")

    alive = "ALIVE" if exe_manager.executable_is_found(exe_name) else "NOT_FOUND"

    alive = {"HEART_BEAT": alive}

    return jsonify(alive)


###############################################################################
###############################################################################
## Supported Game Related Endpoints
###############################################################################
###############################################################################


###############################################################################
###############################################################################
## Key/Access Related Endpoints
###############################################################################
###############################################################################


@application.route("/key/generate", methods=["POST"])
def key_generate():
    logger.info("Host Generating Control Key")
    return "Success"


@application.route("/key/verify", methods=["POST"])
def key_verify():
    logger.info("Host Key Verification - Checking....")
    return "Success"
