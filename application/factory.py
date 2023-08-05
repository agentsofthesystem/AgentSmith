import os

from flask import Flask

from application.common import logger
from application.config.config import DefaultConfig
from application.debugger import init_debugger
from application.api.v1.blueprints.access import access
from application.api.v1.blueprints.executable import executable
from application.api.v1.blueprints.game import game
from application.api.v1.blueprints.steam import steam


def create_app(config=None):
    logger.info(f"Begin initialization.")

    if config is None:
        config = DefaultConfig("python")
        logger.critical("WARNING. Missing Configuration. Initializing with default...")

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

    # Register all blueprints
    app.register_blueprint(access)
    app.register_blueprint(executable)
    app.register_blueprint(game)
    app.register_blueprint(steam)

    @app.before_request
    def before_request_func():
        print("Executing Before Request Funcion!")

    logger.info(f"{app.config['APP_NAME']} has successfully initialized.")

    return app
