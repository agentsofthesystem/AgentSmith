import os
import inspect
import importlib.util

from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
)
from PyQt5.QtCore import Qt

from application.api.v1.source import games
from client import Client


@staticmethod
def _find_conforming_modules(package):
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


class NewGameWidget(QWidget):
    """
    The goal of this class is to dynamically inspect the source/games folder
    in the application code and determine the number of classes that implement the
    BaseGame object.  That way the gui maintains itself. Nothing is hard coded.
    """

    def __init__(self, client: Client, parent: QWidget):
        super(QWidget, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._client = client
        self._supported_games = {}
        self._current_inputs = None
        self._initialized = False

    def _build_inputs(self, game_name):
        input_frame = QFrame()
        v_layout = QVBoxLayout()

        game_object = self._supported_games[game_name]
        required_args_list = game_object._get_argument_list()

        for arg in required_args_list:
            h_layout = QHBoxLayout()

            arg_label = QLabel(arg)
            arg_text_edit = QLineEdit()

            h_layout.addWidget(arg_label)
            h_layout.addWidget(arg_text_edit)

            v_layout.addLayout(h_layout)

        install_button = QPushButton("Install")
        install_button.clicked.connect(lambda: self._install_game(game_name))
        v_layout.addWidget(install_button)

        input_frame.setLayout(v_layout)
        input_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        input_frame.setLineWidth(1)

        return input_frame

    def init_ui(self):
        self._layout.setAlignment(Qt.AlignTop)

        self._combo_box = QComboBox()

        modules_dict = _find_conforming_modules(games)

        for module_name in modules_dict.keys():
            game_obj = _instantiate_object(module_name, modules_dict[module_name])
            self._supported_games[game_obj._game_pretty_name] = game_obj
            self._combo_box.addItem(game_obj._game_pretty_name)

        self._combo_box.currentTextChanged.connect(self._text_changed)
        self._layout.addWidget(self._combo_box)

        # Separator
        h_sep = QFrame()
        h_sep.setFrameShape(QFrame.HLine)
        self._layout.addWidget(h_sep)

        # Get first game in supported games.
        supported_games = list(self._supported_games.keys())
        self._current_inputs = self._build_inputs(supported_games[0])
        self._layout.addWidget(self._current_inputs)

        self.setLayout(self._layout)

        self._initialized = True

    def _text_changed(self, game_pretty_name):
        print("Text changed:", game_pretty_name)
        old_inputs = self._current_inputs
        old_inputs.hide()
        self._current_inputs = self._build_inputs(game_pretty_name)
        self._layout.replaceWidget(old_inputs, self._current_inputs)

    def _install_game(self, game_name):
        print(f"Installing Game Name: {game_name}")
        # TODO - Implement this bad boy!
