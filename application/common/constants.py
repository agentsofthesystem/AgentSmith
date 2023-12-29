from datetime import datetime
from enum import Enum


class DeployTypes(Enum):
    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    PYTHON = "python"


class FileModes(Enum):
    NOT_A_FILE = 0
    FILE = 1
    DIRECTORY = 2


SETTING_NAME_STEAM_PATH: str = "steam_install_dir"
SETTING_NAME_DEFAULT_PATH: str = "default_install_dir"
SETTING_NAME_APP_SECRET: str = "application_secret"

NUM_SERVER_PROCESSES: int = 2

STARTUP_BATCH_FILE_NAME: str = "startup.bat"
DEFAULT_SECRET = str(datetime.now())
GAME_INSTALL_FOLDER = "games"

LOCALHOST_IP_ADDR = "127.0.0.1"
WAIT_FOR_BACKEND: int = 1

_DeployTypes = DeployTypes
