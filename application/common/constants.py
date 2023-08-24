import platform
from enum import Enum


class DeployTypes(Enum):
    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    PYTHON = "python"


STARTUP_BATCH_FILE_NAME = "startup.bat"

STARTUP_STEAM_SETTING_NAME = "steam_install_dir"
STARTUP_STEAM_INSTALL_DIR = (
    r"C:\STEAM\steam_cmd" if platform.system() == "Windows" else "/opt/steam/steam_cmd"
)

_DeployTypes = DeployTypes
