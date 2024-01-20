import jwt

from datetime import datetime
from flask import Blueprint, request, jsonify
from oauthlib.oauth2 import RequestValidator

from application.common import logger, constants
from application.common.authorization import _verify_bearer_token
from application.common.decorators import authorization_required
from application.common.exceptions import InvalidUsage
from application.extensions import DATABASE
from application.models.settings import Settings
from application.models.tokens import Tokens

access = Blueprint("access", __name__, url_prefix="/v1")

# https://oauthlib.readthedocs.io/en/latest/oauth2/tokens/bearer.html
# https://pyjwt.readthedocs.io/en/latest/usage.html


###############################################################################
###############################################################################
# token/Access Related Endpoints
###############################################################################
###############################################################################
class TokenValidator(RequestValidator):
    def __init__(self, secret, issuer):
        self.secret = secret
        self.issuer = issuer

    def generate_access_token(self, token_name: str):
        token = jwt.encode(
            {
                "iss": self.issuer,  # issuer
                "created": str(datetime.now()),
                "token_name": token_name,
            },
            self.secret,
            algorithm="HS256",
        )
        return token


@access.route("/token/generate", methods=["GET"])
def token_generate():
    logger.info("Host Generating Bearer Token")
    new_token_name = request.args.get("token_name", None, str)

    if new_token_name is None:
        raise InvalidUsage("Error: Must supply token_name arg", status_code=400)

    token_obj = Tokens.query.filter_by(
        token_name=new_token_name, token_active=True
    ).first()

    if token_obj:
        raise InvalidUsage("Error: Token by that name already exists!", status_code=400)

    secret_obj = Settings.query.filter_by(
        setting_name=constants.SETTING_NAME_APP_SECRET
    ).first()

    validator = TokenValidator(secret_obj.setting_value, constants.APP_NAME)

    computed_token = validator.generate_access_token(new_token_name)

    new_token = Tokens()
    new_token.token_active = True
    new_token.token_name = new_token_name
    new_token.token_value = computed_token

    try:
        DATABASE.session.add(new_token)
        DATABASE.session.commit()
    except Exception as error:
        logger.error(error)
        raise InvalidUsage(
            "Error: Database error while creating new token!", status_code=500
        )

    return computed_token


@access.route("/token/verify", methods=["POST"])
def token_verify():
    logger.info("Host token Verification - Checking....")
    verify_token_name = request.args.get("token_name", None, str)

    if verify_token_name is None:
        raise InvalidUsage("Error: Must supply token_name arg", status_code=400)

    # Check token exists in db and is active
    token_lookup = Tokens.query.filter_by(
        token_active=True, token_name=verify_token_name
    ).first()

    if token_lookup is None:
        raise InvalidUsage(
            "Error: Designate Token does not exist or is inactive.", status_code=403
        )

    # Now actually verify the bearer token embedded in the request.
    # Not using the decorator on purpose in this endpoint.
    status_code = _verify_bearer_token(request)

    if status_code == 200:
        return "Success! Token is valid", 200
    elif status_code == 401:
        return "Error: Invalid Authorization", 401
    elif status_code == 403:
        return "Error: Not Authorization", 403
    else:
        return "Internal Error", 500


@access.route("/token/invalidate", methods=["POST"])
@authorization_required
def token_invalidate():
    logger.info("Invalidating token...")
    token_to_invalidate = request.args.get("token_name", None, str)

    if token_to_invalidate is None:
        raise InvalidUsage("Error: Must supply token_name arg", status_code=400)

    # Check token exists in db and is active
    token_lookup_qry = Tokens.query.filter_by(
        token_active=True, token_name=token_to_invalidate
    )

    if token_lookup_qry.first() is None:
        raise InvalidUsage("Error: Token does not exist!", status_code=400)

    try:
        token_lookup_qry.update({"token_active": False})
        DATABASE.session.commit()
    except Exception as error:
        logger.error(error)
        raise InvalidUsage(
            "Error: Database error while invalidating token!", status_code=500
        )

    return "Success", 200


@access.route("/tokens", methods=["GET"])
@authorization_required
def get_all_tokens():
    logger.info("Retrieving all active tokens...")
    tokens = Tokens.query.filter_by(token_active=True)
    token_data = Tokens.to_collection_dict(
        tokens, 1, 1000000000, "access.get_all_tokens"
    )

    token_items = token_data["items"]

    for token in token_items:
        token.pop("token_value")

    return jsonify(token_data)
