import os

from alembic import command
from alembic.config import Config
from flask import Flask

from application.common import logger, constants, toolbox
from application.config.config import DefaultConfig
from application.debugger import init_debugger
from application.extensions import DATABASE
from application.api.v1.blueprints.access import access
from application.api.v1.blueprints.app import app
from application.api.v1.blueprints.architect import architect
from application.api.v1.blueprints.game import game
from application.api.v1.blueprints.steam import steam
from application.models.games import Games
from application.models.settings import Settings

CURRENT_FOLDER = toolbox._get_application_path()
STATIC_FOLDER = os.path.join(CURRENT_FOLDER, "static")
TEMPLATE_FOLDER = os.path.join(CURRENT_FOLDER, "templates")
ALEMBIC_FOLDER = os.path.join(CURRENT_FOLDER, "alembic")


def _startup_checks():
    # Make sure game state is accurage.
    installed_games = Games.query.all()

    # Keep track of the number of updates.
    num_updates = 0

    for this_game in installed_games:
        # The DB has a PID for the game.
        if this_game.game_pid:
            # Check that the game is actually running. If not, delete the PID.
            game_object = toolbox._get_supported_game_object(this_game.game_name)
            if not toolbox._get_proc_by_name(game_object._game_executable):
                game_qry = Games.query.filter_by(game_id=this_game.game_id)
                game_qry.update({"game_pid": None})
                num_updates += 1

    # Only update database if needed.
    if num_updates > 0:
        DATABASE.session.commit()


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
        constants.APP_NAME,
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
    flask_app.register_blueprint(architect)
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
            constants.DEFAULT_INSTALL_PATH, "steam"
        ),
        constants.SETTING_NAME_DEFAULT_PATH: constants.DEFAULT_INSTALL_PATH,
        constants.SETTING_NAME_APP_SECRET: flask_app.config["APP_DEFAULT_SECRET"],
        constants.SETTING_NGINX_PROXY_PORT: flask_app.config["NGINX_DEFAULT_PORT"],
        constants.SETTING_NGINX_PROXY_HOSTNAME: flask_app.config[
            "NGINX_DEFAULT_HOSTNAME"
        ],
        constants.SETTING_NGINX_ENABLE: flask_app.config["NGINX_DEFAULT_ENABLED"],
    }

    with flask_app.app_context():
        # Here just going to initialize some settings. TODO - Make into a function.
        for setting_name, setting_value in startup_settings.items():
            setting_obj = Settings.query.filter_by(setting_name=setting_name).first()

            if setting_obj is None:
                new_setting = Settings()
                new_setting.setting_name = setting_name
                new_setting.setting_value = setting_value
                DATABASE.session.add(new_setting)
                DATABASE.session.commit()

        # Run other startup checks.
        _startup_checks()

    logger.info(f"{constants.APP_NAME} has been successfully created.")

    return flask_app
