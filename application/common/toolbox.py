import os
import inspect
import importlib.util
import psutil

from flask import request

from application.common.exceptions import InvalidUsage
from application.source.models.games import Games
from application.source.models.game_arguments import GamesArguments


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
        proc_name = proc.name()

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
def get_games_schema():
    valid_cols = []

    for column in Games.__table__.columns:
        valid_cols.append(column.name)

    return valid_cols


@staticmethod
def get_all_games():
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", 10, type=int), 10000
    )  # TODO Replace update limit
    return Games.to_collection_dict(Games.query, page, per_page, "game.get_all_games")


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
def _instantiate_object(module_name, module):
    return_obj = None
    for item in inspect.getmembers(module, inspect.isclass):
        if item[1].__module__ == module_name:
            return_obj = item[1]()
    return return_obj
