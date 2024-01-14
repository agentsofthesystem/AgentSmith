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
        # Extract headers & Confirm
        request_headers = request.headers
        force_auth = current_app.config["FLASK_FORCE_AUTH"]
        disable_auth = current_app.config["FLASK_DISABLE_AUTH"]

        # If NGINX is in the loop, then X-Forwarded-Host will be populated in the request header
        # That is the desired IP address to use to determine whether or not to enforce
        # authentication.
        if "X-Forwarded-Host" in request_headers:
            request_addr = request_headers["X-Forwarded-Host"]

            # Someone, in theory, could fake this and provide 127.0.0.1 as the X-Forwarded-Host,
            # check for that.
            if "127.0.0.1" == request_addr:
                logger.error(
                    "Authorization: Invalid attempt to pass 127.0.0.1 for X-Forwarded-Host"
                )
                return "Error: Bad Request", 400

            logger.debug("Using X-Forwarded-Host for IP address.")
        else:
            request_addr = request.remote_addr
            logger.debug("Using request.remote_addr for IP address.")

        logger.debug(f"Remote IP: {request_addr}")

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
