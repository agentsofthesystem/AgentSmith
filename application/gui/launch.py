import os
import time

from flask import Flask
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QSystemTrayIcon, QMenu, QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from threading import Thread

from application.config.config import DefaultConfig
from application.common import logger, constants
from application.common.decorators import timeit
from application.common.toolbox import _get_application_path
from application.gui.globals import GuiGlobals
from application.gui.game_install_window import GameInstallWindow
from application.gui.game_manager_window import GameManagerWindow
from application.gui.intalled_games_menu import InstalledGameMenu
from application.gui.widgets.add_argument_widget import AddArgumentWidget
from application.gui.widgets.settings_widget import SettingsWidget
from application.managers.nginx_manager import NginxManager
from application.factory import create_app
from operator_client import Operator


class GuiApp:
    REFRESH_INTERVAL = 60 * constants.MILIS_PER_SECOND

    def __init__(self, globals_obj: GuiGlobals) -> None:
        # Globals
        self._globals = globals_obj
        self._globals._FLASK_APP = self._create_backend()
        self._globals._client = Operator(
            "http://" + self._globals._server_host,
            self._globals._server_port,
            verbose=False,
            timeout=10,
        )
        self._globals._nginx_manager = NginxManager(self._globals._client)

        # Declare variables
        self._gui_app = QApplication([])
        self._server_thread = None
        self._main_menu = QMenu()
        self._installed_games_menu = None
        self._game_manager_window = None
        self._globals._global_clipboard = self._gui_app.clipboard()

        # Time to update this class widget
        self._timer: QTimer = QTimer()
        self._timer.timeout.connect(self._refresh_on_timer)

    @timeit
    def _create_backend(self) -> Flask:
        config = DefaultConfig("python")
        config.obtain_environment_variables()

        app = create_app(config=config)
        app.debug = False
        app.config["ENV"] = "production"

        return app

    @timeit
    def _spawn_server_on_thread(self):
        self._server_thread = Thread(
            target=lambda: self._globals._FLASK_APP.run(
                host="127.0.0.1",  # Only accept connections via localhost.
                port=constants.FLASK_SERVER_PORT,
                debug=False,
                use_reloader=False,
                threaded=True,
                use_evalex=False,
            )
        )
        self._server_thread.daemon = True

        self._server_thread.start()

    def quit_gui(self):
        self._globals._nginx_manager.shutdown()
        self._gui_app.quit()

    def _launch_game_manager_window(self):
        # This has to be the current games, not init data.
        all_games = self._globals._client.game.get_games()

        # Error checking. If backend server goes down, don't want to crash.
        if all_games is None:
            logger.critical(
                "GuiApp::_launch_game_manager_window - Error - Is Server Offline?"
            )
            return

        if len(all_games["items"]) == 0:
            message = QMessageBox()
            message.setText("Please install a game before using the Game Manager!")
            message.exec()
            return

        if not self._game_manager_window._initialized:
            self._game_manager_window.init_ui()
        else:
            self._game_manager_window.update()

        self._game_manager_window.showWindow()

    def _launch_new_game_window(self):
        if not self._game_install_window._initialized:
            self._game_install_window.init_ui()
        self._game_install_window.show()

    def _launch_settings_widget(self):
        if not self._settings_widget._initialized:
            self._settings_widget.init_ui()
        self._settings_widget.show()

    def _refresh_on_timer(self):
        # Refresh the quick actions menu to capture any potential game state changes.
        logger.debug("System Tray App: Updating Quick Action Menu.")
        self._installed_games_menu.update_menu_list()

    def initialize(self, with_server=False):
        # If running the unified launch script, this will need to start up first.

        initialization_data = None

        if with_server:
            # Check that one is not already running.
            is_already_there = None
            is_already_there = self._globals._client.architect.get_health()
            if is_already_there == "Alive":
                message = QMessageBox()
                message.setText(
                    "Error: Unable to start. This application is already running!"
                )
                message.exec()
                return

            # Launch Flask Server
            self._spawn_server_on_thread()

            # Give server a chance to start before proceeding...
            time.sleep(1)

        initialization_data = self._globals._client.app.get_gui_initialization_data()

        if initialization_data is None:
            message = QMessageBox()
            message.setText(
                "Error: The backend Agent Software is not responding. Unable to start up."
            )
            message.exec()
            return

        self._globals.set_initialization_data(initialization_data)

        nginx_enable = self._globals._init_settings_data[constants.SETTING_NGINX_ENABLE]

        # DB Stores as string so quick conversion to boolean.
        nginx_enable = True if nginx_enable == "1" else False

        # Generate SSL key pair if non-existant.
        if not self._globals._nginx_manager.key_pair_exists():
            logger.debug(
                "Warning: No nginx key pair found, creating a new SSL certificate pair."
            )
            self._globals._nginx_manager.generate_ssl_certificate(
                initialize=self._globals._init_settings_data
            )

        # Launch Reverse Proxy Server if enabled.
        if nginx_enable:
            self._globals._nginx_manager.startup(
                initialize=self._globals._init_settings_data
            )

        # Instantiate this last always!
        self._installed_games_menu = InstalledGameMenu(
            self._main_menu, self._globals._client, self._globals._init_games_data
        )
        self._add_arguments_widget = AddArgumentWidget(self._globals._client)

        # Assign those widgets to global before instantiating other windows.
        self._globals._add_arguments_widget = self._add_arguments_widget
        self._globals._installed_games_menu = self._installed_games_menu

        self._game_manager_window = GameManagerWindow(self._globals)
        self._game_install_window = GameInstallWindow(self._globals)
        self._settings_widget = SettingsWidget(self._globals._client, self._globals)

        self._gui_app.setQuitOnLastWindowClosed(False)

        # Adding an icon
        icon_path = os.path.join(
            _get_application_path(), "gui", "resources", "agent-green.png"
        )
        logger.debug(f"Expecting Icon Path to be: {icon_path}")
        icon = QIcon(icon_path)

        # Adding item on the menu bar
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        # Creating the options
        game_manager = QAction("Game Manager")
        game_manager.triggered.connect(self._launch_game_manager_window)
        self._main_menu.addAction(game_manager)

        self._main_menu.addSeparator()

        game_install = QAction("New Game")
        game_install.triggered.connect(self._launch_new_game_window)
        self._main_menu.addAction(game_install)

        # Installed Games Menu & Submenues.
        self._main_menu.addMenu(self._installed_games_menu)

        self._main_menu.addSeparator()

        # Overall app settings
        settings = QAction("Settings")
        settings.triggered.connect(self._launch_settings_widget)
        self._main_menu.addAction(settings)

        # To quit the app
        quit = QAction("Quit")
        quit.triggered.connect(self.quit_gui)
        self._main_menu.addAction(quit)

        tray.setContextMenu(self._main_menu)

        self._timer.setInterval(self.REFRESH_INTERVAL)
        self._timer.start()

        self._gui_app.exec_()
