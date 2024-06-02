import jwt

from flask.wrappers import Request

from application.common import constants
from application.models.settings import Settings
from application.models.tokens import Tokens


def _get_token(bearer_token: str) -> Tokens:
    token_lookup = Tokens.query.filter_by(
        token_active=True, token_value=bearer_token
    ).first()
    return token_lookup


def _get_setting(setting_name: str) -> Settings:
    setting_lookup = Settings.query.filter_by(setting_name=setting_name).first()
    return setting_lookup


def _verify_bearer_token(request: Request) -> int:
    """This is the bearer token gauntlet.
    The requests only goal is to get through all of the checks.
    """
    # Use 401 Unauthorized if token is missing entirely, 403 its there but not allowed.
    headers = request.headers

    if "Authorization" not in headers:
        return 401

    auth = headers["Authorization"]

    if "Bearer" not in auth:
        return 401

    bearer_token = auth.split("Bearer")[-1].strip()

    # Make sure it's there first...
    token_lookup = _get_token(bearer_token)

    if token_lookup is None:
        return 403

    # Next decode this bad thing...
    secret_obj = _get_setting(constants.SETTING_NAME_APP_SECRET)

    try:
        decoded_token = jwt.decode(
            bearer_token, secret_obj.setting_value, algorithms="HS256"
        )
    except jwt.exceptions.DecodeError:
        return 403

    # Last check... better equal what's in the database.
    decoded_token_name = decoded_token["token_name"]
    if decoded_token_name != token_lookup.token_name:
        return 403

    return 200
