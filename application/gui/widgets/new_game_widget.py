import os
import time

from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QLabel,
    QLayout,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from application.common import constants, toolbox, logger
from application.common.game_argument import GameArgument
from application.common.game_base import BaseGame
from application.gui.globals import GuiGlobals
from application.gui.widgets.file_select_widget import FileSelectWidget
from application.gui.widgets.game_arguments_widget import GameArgumentsWidget
from application import games


class NewGameWidget(QWidget):
    """
    The goal of this class is to dynamically inspect the source/games folder
    in the application code and determine the number of classes that implement the
    BaseGame object.  That way the gui maintains itself. Nothing is hard coded.
    """

    def __init__(self, globals: GuiGlobals, parent: QWidget):
        super(QWidget, self).__init__(parent)

        self._layout = QVBoxLayout()
        self._layout.sizeConstraint = QLayout.SetDefaultConstraint

        self._globals: GuiGlobals = globals
        self._client = globals._client
        self._install_games_menu = globals._installed_games_menu
        self._supported_games: dict = {}
        self._arg_widget: GameArgumentsWidget = None

        self._current_inputs = None
        self._current_args_dict: dict = {}
        self._current_game_install_path: FileSelectWidget = FileSelectWidget(
            self._client, constants.FileModes.DIRECTORY, self
        )

        self._default_install_dir: str = self._globals._init_settings_data[
            constants.SETTING_NAME_DEFAULT_PATH
        ]

        self._defaults: dict = {
            constants.SETTING_NAME_DEFAULT_PATH: self._default_install_dir
        }

        self._initialized = False

    def _build_inputs(self, game_name):
        input_frame = QFrame()

        input_frame_main_layout = QVBoxLayout()
        input_frame_path_layout = QHBoxLayout()

        game_object: BaseGame = self._supported_games[game_name]
        game_short_name = game_object._game_name
        required_args_dict = game_object._get_argument_dict()
        args_list = []

        for arg, arg_obj in required_args_dict.items():
            arg_dict = {}
            arg_dict["game_arg"] = arg
            arg_dict["required"] = arg_obj._required
            if arg_obj._value is None:
                arg_dict["game_arg_value"] = ""  # Should be empty string
            else:
                arg_dict["game_arg_value"] = arg_obj._value  # Should be empty string
            arg_dict["file_mode"] = arg_obj._file_mode
            arg_dict["is_permanent"] = arg_obj._is_permanent
            args_list.append(arg_dict)

        disabled_cols = ["Required", "Actions"]

        self._arg_widget = GameArgumentsWidget(
            self._client, args_list, input_frame, disable_cols=disabled_cols
        )
        self._arg_widget.disable_horizontal_scroll()

        input_frame_main_layout.addWidget(self._arg_widget)

        # Separate game info from game arguments
        h_sep = QFrame()
        h_sep.setFrameShape(QFrame.HLine)

        # Compute a default game installation directory.
        game_install_path = os.path.join(
            self._default_install_dir, constants.GAME_INSTALL_FOLDER, game_short_name
        )

        # Add install path
        install_path_layout = QHBoxLayout()
        label = QLabel("Game Install Path: ")
        text_edit = FileSelectWidget(
            self._client,
            constants.FileModes.DIRECTORY,
            self,
            default_path=game_install_path,
        )
        self._current_game_install_path = text_edit
        install_path_layout.addWidget(label)
        install_path_layout.addWidget(text_edit)
        input_frame_path_layout.addLayout(install_path_layout)

        # combine args and input path
        input_frame_main_layout.addWidget(h_sep)
        input_frame_main_layout.addLayout(input_frame_path_layout)

        # installation button
        install_button = QPushButton("Install Game Server")
        install_button.clicked.connect(lambda: self._install_game(game_name))
        input_frame_main_layout.addWidget(install_button)

        input_frame.setLayout(input_frame_main_layout)
        input_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        input_frame.setLineWidth(1)
        input_frame.adjustSize()

        return input_frame

    def init_ui(self):
        self._layout.setAlignment(Qt.AlignTop)

        self._combo_box = QComboBox()

        modules_dict = toolbox._find_conforming_modules(games)

        for module_name in modules_dict.keys():
            game_obj = toolbox._instantiate_object(
                module_name, modules_dict[module_name], self._defaults
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

        self.adjustSize()
        self.parentWidget().adjustSize()

        self.show()

        self._initialized = True

    def _text_changed(self, game_pretty_name):
        logger.info(f"Curent Game changed to: {game_pretty_name}")
        old_inputs = self._current_inputs
        old_inputs.hide()
        self._current_args_dict = {}
        self._current_game_install_path = FileSelectWidget(
            self._client, constants.FileModes.DIRECTORY, self
        )
        self._current_inputs = self._build_inputs(game_pretty_name)
        self._layout.replaceWidget(old_inputs, self._current_inputs)
        self.adjustSize()
        self.parentWidget().adjustSize()

    def _install_game(self, game_pretty_name):
        logger.info(f"Installing Game Name: {game_pretty_name}")

        input_dict = {}
        game_object: BaseGame = self._supported_games[game_pretty_name]
        steam_id = game_object._game_steam_id
        game_name = game_object._game_name  # Get regular name. Not the pretty name.
        default_argument_dict = game_object._get_argument_dict()
        self._current_args_dict = (
            self._arg_widget.get_args_dict()
        )  # What the user actually input.
        install_path = self._current_game_install_path.get_line_edit().text()
        steam_install_dir = self._client.app.get_setting_by_name(
            constants.SETTING_NAME_STEAM_PATH
        )

        # Check if game already exists
        game_data = self._client.game.get_game_by_name(game_name)
        is_game_present = True if len(game_data["items"]) > 0 else False

        # If the game server is already installed, then let the user know.
        if is_game_present:
            message = QMessageBox()
            message.setText(
                "Error: That game was already installed! "
                "Multiple Same Server installs not yet supported."
            )
            message.exec()
            return

        message = QMessageBox(self)
        message.setWindowTitle("Installing ... ")
        message.setText(
            f"Installing {game_pretty_name}. You will be notified when the process is finished. "
            "Please click okay to continue..."
        )
        message.exec()

        if install_path == "":
            message = QMessageBox()
            message.setText("Error: Must supply an install path. Try again!")
            message.exec()
            return

        for arg in self._current_args_dict.keys():
            line_edit = self._current_args_dict[arg]

            if line_edit.text() == "":
                message = QMessageBox()
                message.setText(
                    f"Error: Must supply a value for Argument, {arg}. Try again!"
                )
                message.exec()
                return

            input_dict[arg] = line_edit.text()

        thread_ident = self._client.steam.install_steam_app(
            steam_install_dir,
            steam_id,
            install_path,
        )
        thread_alive = self._client.app.is_thread_alive(thread_ident)

        logger.debug(f"Install Thread Ident: {thread_ident}, Alive: {thread_alive}")

        while thread_alive:
            logger.debug("Waiting for installation to finish....")
            thread_alive = self._client.app.is_thread_alive(thread_ident)
            time.sleep(1)

        # Add arguments after install
        for arg_name, arg_val in input_dict.items():
            arg_object: GameArgument = default_argument_dict[
                arg_name
            ]  # Use this to get other attributes.
            self._client.game.create_argument(
                game_name,
                arg_name,
                arg_val,
                is_permanent=arg_object._is_permanent,
                required=arg_object._required,
                file_mode=arg_object._file_mode,
                use_equals=arg_object._use_equals,
                use_quotes=arg_object._use_quotes,
            )

        self._install_games_menu.update_menu_list()

        # Get the game now, that it's been installed.
        game_data = self._client.game.get_game_by_name(game_name)
        game_id = game_data["items"][0]["game_id"]

        steam_build_id = self._client.steam.get_steam_app_build_id(
            steam_install_dir, install_path, steam_id
        )

        if steam_build_id:
            self._client.game.update_game_data(
                game_id, game_steam_build_id=steam_build_id
            )

        message = QMessageBox(self)
        message.setWindowTitle("Complete")
        message.setText(f"Installation of {game_pretty_name}, complete!")
        message.exec()
