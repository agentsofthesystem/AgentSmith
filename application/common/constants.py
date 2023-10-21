import platform

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


STARTUP_BATCH_FILE_NAME: str = "startup.bat"
DEFAULT_SECRET = str(datetime.now())

STARTUP_SETTINGS: dict = {
    "steam_install_dir": r"C:\STEAM_TEST\steam"
    if platform.system() == "Windows"
    else "/opt/steam/steam_cmd",
    "application_secret": DEFAULT_SECRET,
}

LOCALHOST_IP_ADDR = "127.0.0.1"
WAIT_FOR_BACKEND: int = 1

_DeployTypes = DeployTypes
