from flask import Blueprint, jsonify
from application.common import logger

app = Blueprint("app", __name__, url_prefix="/v1")


@app.route("/health", methods=["GET"])
def health():
    logger.info("App is alive!")
    return jsonify("Alive")
