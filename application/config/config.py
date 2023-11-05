import os
import platform

from application.common import logger
from application.common.constants import _DeployTypes


class DefaultConfig:
    # App name and secret
    APP_NAME = "AgentSmith"
    APP_PRETTY_NAME = "Agent Smith"
    DEPLOYMENT_TYPE = "python"  # also supports kubernetes

    # Flask specific configs
    DEBUG = True
    ENV = "development"
    FLASK_RUN_HOST = "0.0.0.0"
    FLASK_RUN_PORT = "3000"
    FLASK_FORCE_AUTH = False  # Leave as False except in testing.

    # Designate where the database file is stored based on platform.
    if platform.system() == "Windows":
        base_folder = f"C:\\{APP_NAME}"
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{base_folder}\\{APP_NAME}.db"
    else:
        # Linux
        # Right now, this is for testing since GitHub actions uses linux
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{APP_NAME}.db"

    def __init__(self, deploy_type):
        configuration_options = [el.value for el in _DeployTypes]

        if deploy_type not in configuration_options:
            logger.info(
                f"Configuration: {deploy_type} is not a valid configuration type, which are: {configuration_options}"
            )
            raise RuntimeError

        self.DEPLOYMENT_TYPE = deploy_type

    @classmethod
    def obtain_environment_variables(cls):
        for var in cls.__dict__.keys():
            if var[:1] != "_" and var != "obtain_environment_variables":
                if var in os.environ:
                    value = os.environ[var].lower()
                    if value == "true" or value == "TRUE" or value == "True":
                        setattr(cls, var, True)
                    elif value == "false" or value == "FALSE" or value == "False":
                        setattr(cls, var, False)
                    else:
                        setattr(cls, var, os.environ[var])

    @classmethod
    def __str__(cls):
        print_str = ""
        for var in cls.__dict__.keys():
            if var[:1] != "_" and var != "obtain_environment_variables":
                print_str += f"VAR: {var} set to: {getattr(cls,var)}\n"
        return print_str
