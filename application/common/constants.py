import logging
import platform

from datetime import datetime
from enum import Enum

APP_NAME = "AgentSmith"


class DeployTypes(Enum):
    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    PYTHON = "python"


class GameActionTypes(Enum):
    INSTALLING = "installing"
    UPDATING = "updating"
    STARTING = "starting"
    STOPPING = "stopping"
    RESTARTING = "restarting"
    UNINSTALLING = "uninstalling"


class GameStates(Enum):
    NOT_STATE = "NO_STATE"
    INSTALL_FAILED = "install_failed"
    UPDATE_FAILED = "update_failed"
    STARTED = "started"
    STARTUP_FAILED = "startup_failed"
    STOPPED = "stopped"
    SHUTDOWN_FAILED = "shutdown_failed"
    UNINSTALL_FAILED = "uninstall_failed"


class FileModes(Enum):
    NOT_A_FILE = 0
    FILE = 1
    DIRECTORY = 2


if platform.system() == "Windows":
    DEFAULT_INSTALL_PATH = f"C:\\{APP_NAME}"
    SSL_FOLDER = f"C:\\{APP_NAME}\\ssl"
    SSL_KEY_FILE = f"C:\\{APP_NAME}\\ssl\\private.key"
    SSL_CERT_FILE = f"C:\\{APP_NAME}\\ssl\\selfsigned.crt"
else:
    # TODO - Revisit this when linux support gets closer...
    DEFAULT_INSTALL_PATH = f"/usr/local/share/{APP_NAME}"

# Settings
SETTING_NAME_STEAM_PATH: str = "steam_install_dir"
SETTING_NAME_DEFAULT_PATH: str = "default_install_dir"
SETTING_NAME_APP_SECRET: str = "application_secret"
SETTING_NGINX_PROXY_PORT: str = "nginx_proxy_port"
SETTING_NGINX_PROXY_HOSTNAME: str = "nginx_proxy_hostname"
SETTING_NGINX_ENABLE: str = "nginx_enable"

# Nginx
NGINX_VERSION = "nginx-1.24.0"
NGINX_STABLE_RELEASE_WIN = f"https://nginx.org/download/{NGINX_VERSION}.zip"

# Other / Misc
STARTUP_BATCH_FILE_NAME: str = "startup.bat"
DEFAULT_SECRET = str(datetime.now())
GAME_INSTALL_FOLDER = "games"
LOCALHOST_IP_ADDR = "127.0.0.1"
WAIT_FOR_BACKEND: int = 1
FLASK_SERVER_PORT: int = 5000
MILIS_PER_SECOND = 1000
BYTES_PER_KB = 1024
KB_PER_MB = 1024

# Logging
DEFAULT_LOG_LEVEL = logging.NOTSET
DEFAULT_LOG_DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"
DEFAULT_LOG_FORMAT = "%(filename)s:%(lineno)s %(levelname)s:%(message)s"
DEFAULT_LOG_SIZE_BYTES = 1024 * KB_PER_MB * 64  # MB

# Controls not meant to be hooked up to GUI. Just for dev/debug:
ENABLE_TIMEIT_PRINTS = False

_DeployTypes = DeployTypes
