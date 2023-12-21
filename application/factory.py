import os

from alembic import command
from alembic.config import Config
from flask import Flask

from application.common import logger, constants
from application.common.toolbox import _get_application_path
from application.config.config import DefaultConfig
from application.debugger import init_debugger
from application.extensions import DATABASE
from application.api.v1.blueprints.access import access
from application.api.v1.blueprints.app import app
from application.api.v1.blueprints.executable import executable
from application.api.v1.blueprints.game import game
from application.api.v1.blueprints.steam import steam
from application.source.models.settings import Settings

CURRENT_FOLDER = _get_application_path()
STATIC_FOLDER = os.path.join(CURRENT_FOLDER, "static")
TEMPLATE_FOLDER = os.path.join(CURRENT_FOLDER, "templates")
ALEMBIC_FOLDER = os.path.join(CURRENT_FOLDER, "source", "alembic")


def _handle_migrations(flask_app: Flask):
    alembic_init = os.path.join(ALEMBIC_FOLDER, "alembic.ini")

    alembic_cfg = Config(alembic_init)

    alembic_cfg.set_section_option(
        alembic_cfg.config_ini_section,
        "sqlalchemy.url",
        flask_app.config["SQLALCHEMY_DATABASE_URI"],
    )

    alembic_cfg.set_section_option(
        alembic_cfg.config_ini_section, "script_location", ALEMBIC_FOLDER
    )
    with flask_app.app_context():
        with DATABASE.engine.begin() as connection:
            alembic_cfg.attributes["connection"] = connection

            command.upgrade(alembic_cfg, "head")


def create_app(config=None):
    logger.info("Begin initialization.")

    if config is None:
        config = DefaultConfig("python")
        logger.critical("WARNING. Missing Configuration. Initializing with default...")

    flask_app = Flask(
        config.APP_NAME,
        instance_relative_config=False,
        static_folder=STATIC_FOLDER,
        static_url_path="/static",
        template_folder=TEMPLATE_FOLDER,
    )

    # Changing instance path to directory above.
    instance_path = os.path.dirname(flask_app.instance_path)
    flask_app.instance_path = instance_path

    flask_app.config.from_object(config)

    # Set up debugging if the user asked for it.
    init_debugger(flask_app)

    # Register all blueprints
    flask_app.register_blueprint(access)
    flask_app.register_blueprint(app)
    flask_app.register_blueprint(executable)
    flask_app.register_blueprint(game)
    flask_app.register_blueprint(steam)

    # Uncoment in a before request function is ever needed.
    # @flask_app.before_request
    # def before_request_func():
    #     logger.info("Executing Before Request Function!")

    DATABASE.init_app(flask_app)

    _handle_migrations(flask_app)

    startup_settings: dict = {
        constants.SETTING_NAME_STEAM_PATH: os.path.join(
            flask_app.config["DEFAULT_INSTALL_PATH"], "steam"
        ),
        constants.SETTING_NAME_DEFAULT_PATH: flask_app.config["DEFAULT_INSTALL_PATH"],
        constants.SETTING_NAME_APP_SECRET: flask_app.config["APP_DEFAULT_SECRET"],
    }

    # Here just going to initialize some settings. TODO - Make into a function.
    with flask_app.app_context():
        for setting_name, setting_value in startup_settings.items():
            setting_obj = Settings.query.filter_by(setting_name=setting_name).first()

            if setting_obj is None:
                new_setting = Settings()
                new_setting.setting_name = setting_name
                new_setting.setting_value = setting_value
                DATABASE.session.add(new_setting)
                DATABASE.session.commit()

    logger.info(f"{flask_app.config['APP_NAME']} has been successfully created.")

    return flask_app
