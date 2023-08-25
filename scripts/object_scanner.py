import os
import sys
import inspect
import importlib
import importlib.util

current_file_path = os.path.abspath(__file__)
parent_folder = os.path.dirname(current_file_path)
app_folder = os.path.dirname(parent_folder)

sys.path.append(app_folder)

from application.source import games


@staticmethod
def _find_conforming_modules(package):
    package_location = games.__path__

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
        bar = spec.loader.exec_module(this_module)

        for x in dir(this_module):
            if inspect.isclass(getattr(this_module, x)):
                if x == "BaseGame":
                    conforming_modules.update({module_name: this_module})
                    break

    return conforming_modules


@staticmethod
def _instantiate_object(module_name, module):
    for item in inspect.getmembers(module, inspect.isclass):
        if item[1].__module__ == module_name:
            return item[1]()


if __name__ == "__main__":
    cm_dict = _find_conforming_modules(games)

    # print(cm_dict)

    modules_found = list(cm_dict.keys())

    for module_name in modules_found:
        obj = _instantiate_object(module_name, cm_dict[module_name])
        print(obj._game_pretty_name)
