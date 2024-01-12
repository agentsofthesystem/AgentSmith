from flask import request, current_app
from functools import wraps
from time import time

from application.common import logger
from application.common.constants import LOCALHOST_IP_ADDR
from application.common.authorization import _verify_bearer_token


def authorization_required(func):
    """Define Decorate to enforce verified users for routes."""

    @wraps(func)
    def decorated_view(*args, **kwargs):
        request_addr = request.remote_addr
        force_auth = current_app.config["FLASK_FORCE_AUTH"]
        disable_auth = current_app.config["FLASK_DISABLE_AUTH"]

        logger.debug(f"Remote IP: {request.remote_addr}")

        if disable_auth:
            logger.debug("Authorization is disabled via configuration setting.")
            return func(*args, **kwargs)

        if request_addr == LOCALHOST_IP_ADDR and not force_auth:
            logger.debug("Request is coming from Localhost, no need to do anything...")
            status_code = 200
        elif request_addr == LOCALHOST_IP_ADDR and force_auth:
            logger.debug(
                "Request is coming from Localhost, but authentication is being forced..."
            )
            status_code = _verify_bearer_token(request)
        else:
            logger.debug("Request is external. Authentication required.")
            status_code = _verify_bearer_token(request)

        if status_code == 200:
            return func(*args, **kwargs)
        elif status_code == 401:
            return "Error: Invalid Authorization", 401
        elif status_code == 403:
            return "Error: Not Authorization", 403
        else:
            return "Internal Error", 500

    return decorated_view


def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.debug(
            "Function: :%r args:[%r, %r] took: %2.4f sec"
            % (f.__name__, args, kw, te - ts)
        )
        return result

    return wrap
