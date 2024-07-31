import time

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QComboBox,
    QHBoxLayout,
    QLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QTimer

from application import games
from application.common import constants, toolbox, logger
from application.common.game_base import BaseGame
from application.gui.widgets.add_argument_widget import AddArgumentWidget
from application.gui.intalled_games_menu import InstalledGameMenu
from application.gui.widgets.game_arguments_widget import GameArgumentsWidget
from operator_client import Operator


class GameManagerWidget(QWidget):
    # The lower this number ,the faster it updates.
    REFRESH_INTERVAL = 6 * constants.MILIS_PER_SECOND
    # Update at this faster interval in certain situations.
    FAST_INTERVAL = 1 * constants.MILIS_PER_SECOND

    def __init__(self, client: Operator, globals, parent: QWidget) -> None:
        super(QWidget, self).__init__(parent)

        self._parent: QWidget = parent
        self._client: Operator = client

        # Complex types
        self._layout = QVBoxLayout()
        self._combo_box = QComboBox()
        self._install_games_menu: InstalledGameMenu = globals._installed_games_menu
        self._current_game_frame: QFrame = None
        self._add_arguments_widget: AddArgumentWidget = globals._add_arguments_widget
        self._current_arg_widget: GameArgumentsWidget = None

        self._add_arguments_widget._parent = self

        # Primitives
        self._installed_supported_games: dict = {}
        self._modules_dict: dict = toolbox._find_conforming_modules(games)
        self._current_game_name: str = None
        self._current_game_exe: str = None

        # Time to update this class widget
        self._timer: QTimer = QTimer(self)
        self._timer.timeout.connect(self._refresh_on_timer)

        # Widget items that need to be tracked.
        self._startup_btn: QPushButton = None
        self._shutdown_btn: QPushButton = None
        self._restart_btn: QPushButton = None
        self._uninstall_btn: QPushButton = None
        self._update_btn: QPushButton = None
        self._add_arg_btn: QPushButton = None
        self._game_pid_label: QLabel = None
        self._game_exe_found_label: QLabel = None
        self._game_current_build: QLabel = None
        self._game_update_required: QLabel = None

    def _get_game_object(self, game_name):
        for module_name in self._modules_dict.keys():
            game_obj = toolbox._instantiate_object(
                module_name, self._modules_dict[module_name]
            )
            if game_obj._game_name == game_name:
                return game_obj
        return None

    def init_ui(self, game_data):
        self._layout.sizeConstraint = QLayout.SetDefaultConstraint
        self._layout.setAlignment(Qt.AlignTop)

        self._layout.addWidget(self._combo_box)

        # Separator
        h_sep = QFrame()
        h_sep.setFrameShape(QFrame.HLine)
        self._layout.addWidget(h_sep)

        # Get first game in supported games.
        self.update_installed_games(game_data=game_data, initialize=True)

        # Current game frame gets created in update_installed_games
        self._layout.addWidget(self._current_game_frame)

        self._combo_box.currentTextChanged.connect(self._text_changed)

        self.setLayout(self._layout)

        # Initially show all buttons disabled until the logic has a chance to determine the server
        # state and show the appropriate set of buttons.
        self._disable_all_btns()

        self.show()

        self.start_timer(override_interval=self.FAST_INTERVAL)

        self._initialized = True

    def stop_timer(self):
        # Stop the timer
        self._timer.stop()

    def start_timer(self, override_interval=None):
        if not self._timer.isActive():
            if override_interval:
                self._timer.start(override_interval)
            else:
                self._timer.setInterval(self.REFRESH_INTERVAL)
                self._timer.start()

    def update_installed_games(
        self, game_data=None, initialize=False, skip_timer=False
    ):
        # Do not want callback to trigger during this update.
        self._combo_box.blockSignals(True)

        if game_data is None:
            game_data = self._client.game.get_games()
            game_data = game_data["items"]

        self._combo_box.clear()
        self._installed_supported_games.clear()

        for game in game_data:
            game_pretty_name = game["game_pretty_name"]
            game_name = game["game_name"]
            game_obj = self._get_game_object(game_name)
            self._installed_supported_games[game_pretty_name] = game_obj
            self._combo_box.addItem(game_obj._game_pretty_name)

        installed_supported_games = list(self._installed_supported_games.keys())

        # Init routine uses this function. Don't want to replace the widget the "first" time.
        if len(installed_supported_games) > 0:
            new_game_frame = self._build_game_frame(installed_supported_games[0])

            if initialize:
                self._current_game_frame = new_game_frame
            else:
                old_game_frame = self._current_game_frame
                old_game_frame.hide()
                self._current_game_frame = new_game_frame
                self._layout.replaceWidget(old_game_frame, self._current_game_frame)
                self.adjustSize()

        # Re-enable callback
        self._combo_box.blockSignals(False)

    def _refresh_on_timer(self):
        # Don't want to make request of API before window has been opened for the first time.
        if not (self._current_game_name and self._current_game_exe):
            return

        response_data = self._client.game.get_game_by_name(self._current_game_name)
        game_data = response_data["items"][0]

        game_pid = game_data["game_pid"]
        game_id = game_data["game_id"]
        current_build_id = game_data["game_steam_build_id"]
        current_build_branch = game_data["game_steam_build_branch"]

        is_game_pid = False

        self._game_current_build.setText(str(current_build_id))
        self._game_build_branch.setText(current_build_branch)

        update_data = self._client.game.check_for_update(game_id)

        if update_data:  # not None
            is_required = update_data["is_required"]
            required_text = "Yes" if is_required else "No"
            self._game_update_required.setText(required_text)
        else:
            self._game_update_required.setText("Unknown")

        if game_pid is None:
            self._game_pid_label.setText("Game PID Not in Database")
            is_game_pid = False
        else:
            self._game_pid_label.setText(f"{game_pid}")
            is_game_pid = True

        is_exe_found = self._executable_is_found(self._current_game_exe)

        if is_exe_found:
            self._game_exe_found_label.setText("Executable Running!")
        else:
            self._game_exe_found_label.setText("Executable Not Found on Host.")

        # Game is running
        if is_game_pid and is_exe_found:
            logger.debug("Game is Running, setting buttins accordingly")
            self._disable_btn(self._startup_btn)
            self._disable_btn(self._uninstall_btn)
            self._disable_btn(self._update_btn)
            self._enable_btn(self._shutdown_btn)
            self._enable_btn(self._restart_btn)
        else:
            # Game is not running
            logger.debug("Game is NOT Running, setting buttins accordingly")
            self._enable_btn(self._startup_btn)
            self._enable_btn(self._uninstall_btn)
            self._enable_btn(self._update_btn)
            self._disable_btn(self._shutdown_btn)
            self._disable_btn(self._restart_btn)

        game_arguments = self._client.game.get_argument_by_game_name(
            self._current_game_name
        )

        self._install_games_menu.update_menu_list()
        self._current_arg_widget.update_arguments_table(game_arguments=game_arguments)

        self._timer.setInterval(self.REFRESH_INTERVAL)

    def _enable_btn(self, btn: QPushButton):
        btn.setStyleSheet("")
        btn.setEnabled(True)

    def _disable_btn(self, btn: QPushButton):
        btn.setStyleSheet("text-decoration: line-through;")
        btn.setEnabled(False)

    def _disable_all_btns(self):
        self._disable_btn(self._startup_btn)
        self._disable_btn(self._uninstall_btn)
        self._disable_btn(self._update_btn)
        self._disable_btn(self._shutdown_btn)
        self._disable_btn(self._restart_btn)

    def _build_game_frame(self, game_name):
        if len(self._installed_supported_games.keys()) == 0:
            self.update_installed_games()

        game_object: BaseGame = self._installed_supported_games[game_name]

        game_frame = QFrame()
        game_frame.sizeConstraint = QLayout.SetDefaultConstraint

        # Main layout box
        game_frame_main_layout = QVBoxLayout()

        # Static Game Information
        game_info_label = QLabel("Game Information:", game_frame)
        game_info_label.setStyleSheet("text-decoration: underline;")
        game_frame_main_layout.addWidget(game_info_label)

        h_layout_all_game_info = QHBoxLayout()
        v_layout_info_labels = QVBoxLayout()
        v_layout_info_info_text = QVBoxLayout()

        v_layout_info_labels.addWidget(QLabel("Game Pretty Name", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Exe Name", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Steam ID", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Build ID", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Build Branch", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Update Required?", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game PID", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Exe Found?", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Info URL", game_frame))

        self._current_game_name = game_object._game_name  # not the pretty name
        self._current_game_exe = game_object._game_executable

        v_layout_info_info_text.addWidget(
            QLabel(game_object._game_pretty_name, game_frame)
        )
        v_layout_info_info_text.addWidget(
            QLabel(game_object._game_executable, game_frame)
        )
        v_layout_info_info_text.addWidget(
            QLabel(game_object._game_steam_id, game_frame)
        )

        self._game_current_build = QLabel("", game_frame)
        self._game_build_branch = QLabel("", game_frame)
        self._game_update_required = QLabel("", game_frame)
        self._game_pid_label = QLabel("", game_frame)
        self._game_exe_found_label = QLabel("", game_frame)

        v_layout_info_info_text.addWidget(self._game_current_build)
        v_layout_info_info_text.addWidget(self._game_build_branch)
        v_layout_info_info_text.addWidget(self._game_update_required)
        v_layout_info_info_text.addWidget(self._game_pid_label)
        v_layout_info_info_text.addWidget(self._game_exe_found_label)

        url_link = (
            f'<a href="{game_object._game_info_url}"> {game_object._game_info_url}</a>'
        )
        game_info_url = QLabel(url_link, game_frame)
        game_info_url.setOpenExternalLinks(True)
        v_layout_info_info_text.addWidget(game_info_url)

        h_layout_all_game_info.addLayout(v_layout_info_labels)
        h_layout_all_game_info.addLayout(v_layout_info_info_text)
        game_frame_main_layout.addLayout(h_layout_all_game_info)

        # Game Arguments
        game_args_label = QLabel("Game Arguments:", game_frame)
        game_args_label.setStyleSheet("text-decoration: underline;")
        built_in_args = game_object._get_argument_list()
        game_args = self._client.game.get_argument_by_game_name(game_object._game_name)
        self._current_arg_widget = GameArgumentsWidget(
            self._client, game_args, game_frame, built_in_args=built_in_args
        )

        game_frame_main_layout.addWidget(game_args_label)
        game_frame_main_layout.addWidget(self._current_arg_widget)

        # Add argument button
        self._add_arg_btn = QPushButton("Add Argument")

        # Disable this button if the game server doesn't allow user to add arguments.
        if not game_object._allow_user_args:
            self._add_arg_btn.setDisabled(True)

        game_frame_main_layout.addWidget(self._add_arg_btn)
        self._add_arg_btn.clicked.connect(
            lambda: self._show_add_argument_widget(self._current_game_name)
        )

        # Game controls
        game_control_label = QLabel("Game Server Controls:", game_frame)
        game_control_label.setStyleSheet("text-decoration: underline;")
        game_frame_main_layout.addWidget(game_control_label)

        game_control_h_layout = QHBoxLayout()

        self._startup_btn = QPushButton("Startup")
        self._startup_btn.clicked.connect(
            lambda: self._startup_game(self._current_game_name)
        )
        self._shutdown_btn = QPushButton("Shutdown")
        self._shutdown_btn.clicked.connect(
            lambda: self._shutdown_game(self._current_game_name)
        )
        self._restart_btn = QPushButton("Restart")
        self._restart_btn.clicked.connect(
            lambda: self._restart_game(self._current_game_name)
        )

        self._update_btn = QPushButton("Update")
        self._update_btn.clicked.connect(
            lambda: self._update_game(self._current_game_name)
        )

        self._uninstall_btn = QPushButton("Uninstall")
        self._uninstall_btn.clicked.connect(
            lambda: self._uninstall_game(self._current_game_name)
        )

        game_control_h_layout.addWidget(self._startup_btn)
        game_control_h_layout.addWidget(self._shutdown_btn)
        game_control_h_layout.addWidget(self._restart_btn)
        game_control_h_layout.addWidget(self._update_btn)
        game_control_h_layout.addWidget(self._uninstall_btn)
        game_frame_main_layout.addLayout(game_control_h_layout)

        # Finalize game frame
        game_frame.setLayout(game_frame_main_layout)
        game_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        game_frame.setLineWidth(1)
        game_frame.adjustSize()

        return game_frame

    def _text_changed(self, game_pretty_name):
        logger.debug(f"Curent Game changed to: {game_pretty_name}")

        if game_pretty_name == "":
            return

        self._current_args_list = []

        # This callback might be triggered in the situation where there never was a current game.
        # Ie. The first game being installed.
        if self._current_game_frame is None:
            logger.debug("Setting first time game frame in game manager window.")
            self._current_game_frame = self._build_game_frame(game_pretty_name)
            self._layout.addWidget(self._current_game_frame)
        else:
            logger.debug("Replacing old game frame in game manager window.")
            old_game_frame = self._current_game_frame
            self._current_game_frame = self._build_game_frame(game_pretty_name)
            old_game_frame.hide()
            self._layout.replaceWidget(old_game_frame, self._current_game_frame)

        self._disable_all_btns()
        self._refresh_on_timer()

    def _executable_is_found(self, exe_name: str) -> bool:
        return True if toolbox._get_proc_by_name(exe_name) else False

    def _show_add_argument_widget(self, game_name):
        logger.info(f"Showing Add Arg Widget for game: {game_name}")
        if not self._add_arguments_widget._initialized:
            self._add_arguments_widget.init_ui(game_name)
        else:
            self._add_arguments_widget.update(game_name)
        self.stop_timer()
        self._add_arguments_widget.show()

    def _startup_game(self, game_name):
        logger.info(f"Staring up game: {game_name}")
        args_list = self._client.game.get_argument_by_game_name(game_name)
        arg_dict = {}

        for arg in args_list:
            arg_dict[arg["game_arg"]] = arg["game_arg_value"]

        self._client.game.game_startup(game_name, input_args=arg_dict)
        self._install_games_menu.update_menu_list()

    def _shutdown_game(self, game_name):
        logger.info(f"Shutting down game: {game_name}")
        self._client.game.game_shutdown(game_name)
        self._install_games_menu.update_menu_list()

    def _restart_game(self, game_name):
        logger.info(f"Restarting game: {game_name}")
        self._client.game.game_shutdown(game_name)
        time.sleep(10)
        args_list = self._client.game.get_argument_by_game_name(game_name)
        arg_dict = {}

        for arg in args_list:
            arg_dict[arg["game_arg"]] = arg["game_arg_value"]

        self._client.game.game_startup(game_name, input_args=arg_dict)

    def _update_game(self, game_name):
        logger.info(f"Updating game: {game_name}")

        message = QMessageBox(self)
        message.setWindowTitle("Updating ... ")
        message.setText(
            "Updating the game server. You will be notified when the process is finished. "
            "Please click okay to continue..."
        )
        message.exec()

        steam_install_dir = self._client.app.get_setting_by_name(
            constants.SETTING_NAME_STEAM_PATH
        )
        game_info = self._client.game.get_game_by_name(game_name)

        game_id = game_info["items"][0]["game_id"]
        steam_id = game_info["items"][0]["game_steam_id"]
        install_path = game_info["items"][0]["game_install_dir"]

        thread_ident = self._client.steam.update_steam_app(
            steam_install_dir, steam_id, install_path
        )
        thread_alive = self._client.app.is_thread_alive(thread_ident)

        logger.debug(f"Update Thread Ident: {thread_ident}, Alive: {thread_alive}")

        while thread_alive:
            logger.debug("Waiting for update to finish....")
            thread_alive = self._client.app.is_thread_alive(thread_ident)
            time.sleep(1)

        steam_build_id = self._client.steam.get_steam_app_build_id(
            steam_install_dir, install_path, steam_id
        )

        if steam_build_id:
            self._client.game.update_game_data(
                game_id, game_steam_build_id=steam_build_id
            )

        message = QMessageBox(self)
        message.setWindowTitle("Complete")
        message.setText("Game Server Update is now complete!")
        message.exec()

    def _uninstall_game(self, game_name):
        logger.info(f"Uninstall game: {game_name}")

        qm = QMessageBox()
        response = qm.question(self, "", "Are you sure?", qm.Yes | qm.No)

        if response == qm.No:
            logger.debug("_uninstall_game: User opted not to uninstall the game.")
            return

        # Stop the regular refresh from happening.
        self.stop_timer()

        message = QMessageBox()
        if self._client.game.uninstall(game_name):
            message.setText(f"Game {game_name} was uninstalled!")
            self.update_installed_games(skip_timer=True)

            installed_supported_games = list(self._installed_supported_games.keys())

            if len(installed_supported_games) == 0:
                self.hide()
                self._parent.hide()
            else:
                self.start_timer(
                    override_interval=self.FAST_INTERVAL
                )  # Turn timer back on

            self._install_games_menu.update_menu_list()

        else:
            message.setText("Error: Unable to uninstall game server...")
        message.exec()
