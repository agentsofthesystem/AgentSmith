import os

from flask import Flask

from application.common import logger, constants
from application.config.config import DefaultConfig
from application.debugger import init_debugger
from application.extensions import DATABASE
from application.api.v1.blueprints.access import access
from application.api.v1.blueprints.app import app
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

    flask_app = Flask(
        config.APP_NAME,
        instance_relative_config=True,
        static_folder=STATIC_FOLDER,
        static_url_path="/static",
        template_folder=TEMPLATE_FOLDER,
    )

    flask_app.config.from_object(config)

    # Set up debugging if the user asked for it.
    init_debugger(flask_app)

    # Register all blueprints
    flask_app.register_blueprint(access)
    flask_app.register_blueprint(app)
    flask_app.register_blueprint(executable)
    flask_app.register_blueprint(game)
    flask_app.register_blueprint(steam)

    # @flask_app.before_request
    # def before_request_func():
    #     print("Executing Before Request Function!")

    DATABASE.init_app(flask_app)

    with flask_app.app_context():
        from application.source.models.games import Games
        from application.source.models.game_arguments import GameArguments
        from application.source.models.settings import Settings

        DATABASE.create_all()

        steam_setting_obj = Settings.query.filter_by(
            setting_name=constants.STARTUP_STEAM_SETTING_NAME
        ).first()

        if steam_setting_obj is None:
            new_setting = Settings()
            new_setting.setting_name = constants.STARTUP_STEAM_SETTING_NAME
            new_setting.setting_value = constants.STARTUP_STEAM_INSTALL_DIR
            DATABASE.session.add(new_setting)
            DATABASE.session.commit()

    logger.info(f"{flask_app.config['APP_NAME']} has been successfully created.")

    return flask_app
