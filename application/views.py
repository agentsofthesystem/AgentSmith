from flask import Blueprint, jsonify
from application.common import logger

application = Blueprint("application", __name__)


# Application Routes
@application.route("/start", methods=["POST"])
def start():
    logger.info("Application has Started")
    return "Success"


@application.route("/stop", methods=["POST"])
def stop():
    logger.info("Application has Stopped")
    return "Success"


@application.route("/restart", methods=["POST"])
def restart():
    logger.info("Application has Restarted")
    return "Success"


@application.route("/key/generate", methods=["POST"])
def generate_key():
    logger.info("Application Generating Control Key")
    return "Success"


@application.route("/key/verify", methods=["POST"])
def generate_key():
    logger.info("Application Key Verifiation - Checking....")
    return "Success"


@application.route("/app/status", methods=["POST"])
def generate_key():
    logger.info("Application has Started")

    status = {"status": "SWEET!"}

    return jsonify(status)
