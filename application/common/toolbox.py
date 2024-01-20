import os
import inspect
import importlib.util
import psutil
import sys

from application.common import logger
from application.common.exceptions import InvalidUsage
from application.common.game_base import BaseGame
from application import games


@staticmethod
def recursive_chmod(parent_path: str) -> None:
    for root, dirs, files in os.walk(parent_path):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o777)
        for f in files:
            os.chmod(os.path.join(root, f), 0o777)


@staticmethod
def _get_proc_by_name(process_name: str):
    process = None
    current_procs = list((p for p in psutil.process_iter()))

    for proc in current_procs:
        try:
            proc_name = proc.name()
        except psutil.NoSuchProcess as error:
            logger.error(error)
            continue

        if proc_name == "" or proc_name == " ":
            continue

        if proc_name == process_name:
            process = proc
            break

    return process


@staticmethod
def get_resources_dir(this_file) -> str:
    current_file = os.path.abspath(this_file)
    current_folder = os.path.dirname(current_file)
    resources_folder = os.path.join(current_folder, "resources")
    return resources_folder


@staticmethod
def _find_conforming_modules(package) -> {}:
    package_location = package.__path__

    files_in_package = os.listdir(package_location[0])

    conforming_modules = {}

    for myfile in files_in_package:
        if myfile == "__init__.py" or myfile == "__pycache__":
            continue

        module_name = myfile.split(".py")[0]
        full_path = os.path.join(package_location[0], myfile)

        if os.path.isdir(full_path):
            continue

        # Load the module from file
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        this_module = importlib.util.module_from_spec(spec)
        _ = spec.loader.exec_module(this_module)

        for x in dir(this_module):
            if inspect.isclass(getattr(this_module, x)):
                if x == "BaseGame":
                    conforming_modules.update({module_name: this_module})
                    break

    return conforming_modules


@staticmethod
def _instantiate_object(module_name, module, defaults_dict={}):
    return_obj = None
    for item in inspect.getmembers(module, inspect.isclass):
        if item[1].__module__ == module_name:
            return_obj = item[1](defaults_dict)
    return return_obj


@staticmethod
def _get_application_path():
    if getattr(sys, "frozen", False):
        application_path = os.path.join(sys._MEIPASS, "application")
    elif __file__:
        current_file = os.path.abspath(__file__)
        application_path = os.path.dirname(os.path.dirname(current_file))
    return application_path


@staticmethod
def _get_supported_game_object(game_name: str) -> BaseGame:
    """
    Instead of hardcoding a bunch of if/elif, can dynamically import the game module,
    and search it for the game_name provided.
    """
    game: BaseGame = None
    supported_game_modules = _find_conforming_modules(games)
    for module_name in supported_game_modules.keys():
        check_game: BaseGame = _instantiate_object(
            module_name, supported_game_modules[module_name]
        )
        if check_game._game_name == game_name:
            game = check_game
            break

    if game is None:
        message = f"/game/startup - Error: {game_name} is not a supported game!"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    return game


@staticmethod
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
