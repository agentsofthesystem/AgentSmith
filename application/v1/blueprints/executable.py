from flask import Blueprint, jsonify, request
from application.common import logger
from application.common.exceptions import InvalidUsage
from application.v1.source.executable_manager import GenericExecutableManager

executable = Blueprint("executable", __name__, url_prefix="/v1")


###############################################################################
###############################################################################
### Generic Executable
###############################################################################
###############################################################################


@executable.route("/exe/launch", methods=["POST"])
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


@executable.route("/exe/kill", methods=["POST"])
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
        message = "Unable to start executable."
        logger.error(message)
        raise InvalidUsage(message, status_code=500)

    logger.info(f"Executable Stopped, {payload['exe_name']}")

    output = {"IS_STOPPED": "TRUE" if is_stopped else "FALSE"}

    return jsonify(output)


@executable.route("/exe/restart", methods=["POST"])
def restart():
    logger.info("Executable has Restarted")
    return "Success"


@executable.route("/exe/status", methods=["GET"])
def executable_status():
    logger.info("Checking on executable status information.")
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


@executable.route("/exe/alive", methods=["GET"])
def is_executable_alive():
    logger.info("Checking on executable heartbeat.")
    exe_name = request.args.get("exe_name", None, str)

    if exe_name is None:
        raise InvalidUsage(
            "Error: Missing Input Argument, 'exe_name'.", status_code=400
        )

    exe_manager = GenericExecutableManager(exe_name, "")

    alive = "ALIVE" if exe_manager.executable_is_found(exe_name) else "NOT_FOUND"

    alive = {"HEART_BEAT": alive}

    return jsonify(alive)
