# -*- coding: utf-8 -*-
import os

from application.common.constants import _DeployTypes


class DefaultConfig:
    # App name and secret
    APP_NAME = "PGSM_AGENT"
    APP_PRETTY_NAME = "Private Game Server Manager - Agent"
    SECRET_KEY = "abc123"
    DEPLOYMENT_TYPE = "docker_compose"  # also supports kubernetes

    # Flask specific configs
    DEBUG = True
    ENV = "development"
    FLASK_RUN_HOST = "0.0.0.0"
    FLASK_RUN_PORT = "3000"

    def __init__(self, deploy_type):
        configuration_options = [el.value for el in _DeployTypes]

        if deploy_type not in configuration_options:
            print(
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
