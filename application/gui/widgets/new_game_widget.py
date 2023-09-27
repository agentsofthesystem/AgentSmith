import time

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
from application.common.game_argument import GameArgument
from application.common.game_base import BaseGame
from application.gui.globals import GuiGlobals
from application.gui.widgets.file_select_widget import FileSelectWidget
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
        self._globals: GuiGlobals = globals
        self._client = globals._client
        self._install_games_menu = globals._installed_games_menu
        self._game_control_widget = globals._game_control_widget
        self._supported_games: dict = {}

        self._current_inputs = None
        self._current_args_list = []
        self._current_game_install_path: FileSelectWidget = FileSelectWidget(
            self._client, constants.FileModes.DIRECTORY, self
        )

        self._initialized = False

    def _build_inputs(self, game_name):
        input_frame = QFrame()

        input_frame_main_layout = QVBoxLayout()
        input_frame_args_layout = QHBoxLayout()
        input_frame_path_layout = QHBoxLayout()

        game_object = self._supported_games[game_name]
        required_args_dict = game_object._get_argument_dict()

        labels_layout = QVBoxLayout()
        line_edits_layout = QVBoxLayout()

        for arg, arg_obj in required_args_dict.items():
            arg_label = QLabel(arg)

            # If the argument is a file or dir, then use file select widget
            # otherwise, a plain qlineedit.
            if arg_obj._file_mode != constants.FileModes.NOT_A_FILE.value:
                if arg_obj._file_mode == constants.FileModes.FILE.value:
                    arg_edit_field = FileSelectWidget(
                        self._client, constants.FileModes.FILE, self
                    )
                elif arg_obj._file_mode == constants.FileModes.DIRECTORY.value:
                    arg_edit_field = FileSelectWidget(
                        self._client, constants.FileModes.DIRECTORY, self
                    )
                else:
                    arg_edit_field = QLineEdit("THERE WAS AN ERROR!!!")
                arg_edit_field.show()
            else:
                arg_edit_field = QLineEdit()

            labels_layout.addWidget(arg_label)
            line_edits_layout.addWidget(arg_edit_field)

            if isinstance(arg_edit_field, FileSelectWidget):
                self._current_args_list.append(
                    {arg_label: arg_edit_field.get_line_edit()}
                )
            else:
                self._current_args_list.append({arg_label: arg_edit_field})

        input_frame_args_layout.addLayout(labels_layout)
        input_frame_args_layout.addLayout(line_edits_layout)

        # Separate game info from game arguments
        h_sep = QFrame()
        h_sep.setFrameShape(QFrame.HLine)

        # Add install path
        install_path_layout = QHBoxLayout()
        label = QLabel("Game Install Path: ")
        text_edit = FileSelectWidget(self._client, constants.FileModes.DIRECTORY, self)
        self._current_game_install_path = text_edit
        install_path_layout.addWidget(label)
        install_path_layout.addWidget(text_edit)
        install_button = QPushButton("Install")
        install_button.clicked.connect(lambda: self._install_game(game_name))
        install_path_layout.addWidget(install_button)
        input_frame_path_layout.addLayout(install_path_layout)

        # combine args and input path
        input_frame_main_layout.addLayout(input_frame_args_layout)
        input_frame_main_layout.addWidget(h_sep)
        input_frame_main_layout.addLayout(input_frame_path_layout)

        input_frame.setLayout(input_frame_main_layout)
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
        self._current_game_install_path = FileSelectWidget(
            self._client, constants.FileModes.DIRECTORY, self
        )
        self._current_inputs = self._build_inputs(game_pretty_name)
        self._layout.replaceWidget(old_inputs, self._current_inputs)

    def _install_game(self, game_pretty_name):
        print(f"Installing Game Name: {game_pretty_name}")

        input_dict = {}
        game_object: BaseGame = self._supported_games[game_pretty_name]
        steam_id = game_object._game_steam_id
        game_name = game_object._game_name  # Get regular name. Not the pretty name.
        argument_dict = game_object._get_argument_dict()
        install_path = self._current_game_install_path.get_line_edit().text()
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

        # print(f"Game Install Path is: {install_path}")
        # print(f"Game Steam Id: {steam_id}")
        # print(f"Steam Install Dir: {steam_install_dir}")
        # print("Input Args:")
        # print(input_dict)

        self._client.steam.install_steam_app(
            # steam_install_dir, steam_id, install_path, input_args=input_dict
            steam_install_dir,
            steam_id,
            install_path,
        )

        # Quick sleep. The client functions return while things are running in background non-blocking style.
        # this is to ensure that the backend added the game record.
        # TODO - Consider adding REST API for sole purpose of adding game instaed of doubling up with steam intall API.
        time.sleep(constants.WAIT_FOR_BACKEND)

        # Add arguments after install
        for arg_name, arg_val in input_dict.items():
            arg_object: GameArgument = argument_dict[arg_name]
            self._client.game.create_argument(
                game_name,
                arg_name,
                arg_val,
                is_permanent=arg_object._is_permanent,
                required=arg_object._required,
                file_mode=arg_object._file_mode,
            )

        self._install_games_menu.update_menu()
        self._game_control_widget.update_installed_games()
