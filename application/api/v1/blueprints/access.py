from flask import Blueprint
from application.common import logger

access = Blueprint("access", __name__, url_prefix="/v1")


###############################################################################
###############################################################################
## Key/Access Related Endpoints
###############################################################################
###############################################################################


@access.route("/key/generate", methods=["POST"])
def key_generate():
    logger.info("Host Generating Control Key")
    return "Success"


@access.route("/key/verify", methods=["POST"])
def key_verify():
    logger.info("Host Key Verification - Checking....")
    return "Success"
