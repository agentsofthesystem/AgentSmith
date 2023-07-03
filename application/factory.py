import os
import sys
import time

from flask import Flask

# from flask_cors import CORS

from application.common import logger
from application.debugger import init_debugger
from application.v1.views import application


def create_app(config=None):
    logger.info(f"Begin initialization.")

    if config is None:
        logger.critical("Error. Cannot initialize without a config object, exiting...")
        sys.exit(1)

    CURRENT_FOLDER = os.path.dirname(__file__)
    STATIC_FOLDER = os.path.join(f"{CURRENT_FOLDER}", "static")
    TEMPLATE_FOLDER = os.path.join(f"{CURRENT_FOLDER}", "templates")

    app = Flask(
        config.APP_NAME,
        instance_relative_config=True,
        static_folder=STATIC_FOLDER,
        static_url_path="/static",
        template_folder=TEMPLATE_FOLDER,
    )

    app.config.from_object(config)

    # Set up debugging if the user asked for it.
    init_debugger(app)

    # Set up CORS
    # CORS(app)

    # Register all blueprints
    app.register_blueprint(application)

    @app.before_request
    def before_request_func():
        print("Executing Before Request Funcion!")

    logger.info(f"{app.config['APP_NAME']} has successfully initialized.")

    return app
