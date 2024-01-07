import os
import time

from flask import Flask
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QSystemTrayIcon, QMenu, QApplication, QMessageBox
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
from application.source.nginx_manager import NginxManager
from application.factory import create_app
from operator_client import Operator


class GuiApp:
    def __init__(self, globals_obj: GuiGlobals) -> None:
        # Globals
        self._globals = globals_obj
        self._globals._FLASK_APP = self._create_backend()
        self._globals._client = Operator(
            "http://" + self._globals._server_host,
            self._globals._server_port,
            verbose=False,
        )
        self._globals._nginx_manager = NginxManager(self._globals._client)

        # Declare variables
        self._gui_app = QApplication([])
        self._server_thread = None
        self._main_menu = QMenu()
        self._installed_games_menu = None
        self._game_manager_window = None
        self._globals._global_clipboard = self._gui_app.clipboard()

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
                host="0.0.0.0",
                port=5000,
                debug=False,
                use_reloader=False,
                threaded=True,
                use_evalex=False,
            )
        )
        self._server_thread.daemon = True

        self._server_thread.start()

    def quit_gui(self):
        self._globals._nginx_manager.shtudown()
        self._gui_app.quit()

    def _launch_game_manager_window(self):
        games = self._globals._client.game.get_games()

        if len(games["items"]) == 0:
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

    def initialize(self, with_server=False):
        # If running the unified launch script, this will need to start up first.
        if with_server:
            # Launch Flask Server
            self._spawn_server_on_thread()

            nginx_enable = self._globals._client.app.get_setting_by_name(
                constants.SETTING_NGINX_ENABLE
            )

            logger.info("*********************************")
            logger.info(f"Nginx Enable is: {nginx_enable}")
            logger.info("*********************************")

            nginx_enable = True if nginx_enable == "1" else False

            logger.info("*********************************")
            logger.info(f"Nginx Enable is: {nginx_enable}")
            logger.info("*********************************")

            # Launch Reverse Proxy Server if enabled.
            if nginx_enable:
                self._globals._nginx_manager.startup()

            # Give server a chance to start before proceeding...
            time.sleep(1)

        # Instantiate this last always!
        self._installed_games_menu = InstalledGameMenu(
            self._main_menu, self._globals._client
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

        self._gui_app.exec_()
