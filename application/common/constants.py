import platform
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

# Initial settings and values.
STARTUP_STEAM_SETTING_NAME: str = "steam_install_dir"
STARTUP_STEAM_INSTALL_DIR: str = (
    r"C:\STEAM_TEST\steam" if platform.system() == "Windows" else "/opt/steam/steam_cmd"
)

WAIT_FOR_BACKEND: int = 1

_DeployTypes = DeployTypes
