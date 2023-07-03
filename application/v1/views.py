from flask import Blueprint, jsonify
from application.common import logger

application = Blueprint("application", __name__, url_prefix="/v1")

## Application Endpoints


@application.route("/app/start", methods=["POST"])
def start():
    logger.info("Application has Started")
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
    logger.info("Application has Started")

    status = {"status": "SWEET!"}

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
