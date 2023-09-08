from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from application.common import constants, toolbox
from application.gui.globals import GuiGlobals
from application.source import games


class NewGameWidget(QWidget):
    """
    The goal of this class is to dynamically inspect the source/games folder
    in the application code and determine the number of classes that implement the
    BaseGame object.  That way the gui maintains itself. Nothing is hard coded.
    """

    def __init__(self, globals: GuiGlobals, parent: QWidget):
        super(QWidget, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._globals = globals
        self._client = globals._client
        self._install_games_menu = globals._installed_games_menu
        self._supported_games = {}

        self._current_inputs = None
        self._current_args_list = []
        self._current_game_install_path = QLineEdit()

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

            self._current_args_list.append({arg_label: arg_text_edit})

            v_layout.addLayout(h_layout)

        h_layout_install_path = QHBoxLayout()
        label = QLabel("Game Install Path: ")
        text_edit = QLineEdit("")
        self._current_game_install_path = text_edit

        h_layout_install_path.addWidget(label)
        h_layout_install_path.addWidget(text_edit)

        v_layout.addLayout(h_layout_install_path)

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

        modules_dict = toolbox._find_conforming_modules(games)

        for module_name in modules_dict.keys():
            game_obj = toolbox._instantiate_object(
                module_name, modules_dict[module_name]
            )
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

        self.show()

        self._initialized = True

    def _text_changed(self, game_pretty_name):
        print("Curent Game changed to:", game_pretty_name)
        old_inputs = self._current_inputs
        old_inputs.hide()
        self._current_args_list = []
        self._current_game_install_path = QLineEdit()
        self._current_inputs = self._build_inputs(game_pretty_name)
        self._layout.replaceWidget(old_inputs, self._current_inputs)

    def _install_game(self, game_name):
        print(f"Installing Game Name: {game_name}")

        input_dict = {}
        game_object = self._supported_games[game_name]
        steam_id = game_object._game_steam_id
        install_path = self._current_game_install_path.text()
        steam_install_dir = self._client.app.get_setting_by_name(
            constants.STARTUP_STEAM_SETTING_NAME
        )

        if install_path == "":
            message = QMessageBox()
            message.setText(f"Error: Must supply an install path. Try again!")
            message.exec()
            return

        for arg in self._current_args_list:
            label = list(arg.keys())[0]
            line_edit = arg[label]

            if line_edit.text() == "":
                message = QMessageBox()
                message.setText(
                    f"Error: Must supply a value for Argument, {label.text()}. Try again!"
                )
                message.exec()
                return

            input_dict[label.text()] = line_edit.text()

        print(f"Game Install Path is: {install_path}")
        print(f"Game Steam Id: {steam_id}")
        print(f"Steam Install Dir: {steam_install_dir}")
        print("Input Args:")
        print(input_dict)

        self._client.steam.install_steam_app(
            steam_install_dir, steam_id, install_path, input_args=input_dict
        )

        self._install_games_menu.update_menu()
