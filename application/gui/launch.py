import os
import requests
import sys

from flask import Flask
from threading import Thread
from PyQt5.QtWidgets import QAction, QSystemTrayIcon, QMenu, QApplication, QMessageBox
from PyQt5.QtGui import QIcon

from application.config.config import DefaultConfig
from application.gui.globals import GuiGlobals
from application.gui.game_manager import GameManagerWindow
from application.factory import create_app
from client import Client


class GuiApp:
    def __init__(self, globals_obj: GuiGlobals) -> None:
        # Globals
        self._globals = globals_obj
        self._globals._FLASK_APP = self._create_backend()
        self._globals._client = Client(
            "http://" + self._globals._server_host,
            self._globals._server_port,
            verbose=False,
        )

        # Declare variables
        self._gui_app = QApplication([])
        self._server_thread = None

        # Instantiate this last always!
        try:
            self._game_manager = GameManagerWindow(self._globals)
        except requests.exceptions.ConnectionError:
            message = QMessageBox()
            message.setText(
                "Error: Unable to start due to backend server being offline. Exiting..."
            )
            message.exec()
            sys.exit(1)

    def _create_backend(self) -> Flask:
        config = DefaultConfig("python")
        config.obtain_environment_variables()

        app = create_app(config=config)
        app.debug = False
        app.config["ENV"] = "production"

        return app

    def _spawn_server_on_thread(self):
        self._server_thread = Thread(
            target=lambda: self._globals._FLASK_APP.run(
                host="0.0.0.0", port=3000, debug=True, use_reloader=False
            )
        )
        self._server_thread.daemon = True

        self._server_thread.start()

    def quit_gui(self):
        self._gui_app.quit()

    def _launch_game_manager(self):
        if not self._game_manager._initialized:
            self._game_manager.init_ui()
        self._game_manager.show()
        self._game_manager._game_summary.update_table()

    def _test_func(self):
        print("Test Function!")

    def initialize(self, with_server=False, testing_mode=False):
        self._gui_app.setQuitOnLastWindowClosed(False)

        # Adding an icon
        current_file = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_file)
        icon_path = os.path.join(current_folder, "resources", "keeper.png")
        print(f"Expecting Icon Path to be: {icon_path}")
        icon = QIcon(icon_path)

        # Adding item on the menu bar
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        # Creating the options

        main_menu = QMenu()

        all_games = QAction("Game Manager")
        all_games.triggered.connect(self._launch_game_manager)
        main_menu.addAction(all_games)

        # Installed Games Menu & Submenues.
        sub_menu1 = QMenu("Installed Games", parent=main_menu)
        installed1 = QAction("Game 1")
        installed2 = QAction("Game 2")
        sub_menu1.addAction(installed1)
        sub_menu1.addAction(installed2)
        main_menu.addMenu(sub_menu1)

        # To quit the app
        quit = QAction("Quit")
        quit.triggered.connect(self.quit_gui)
        main_menu.addAction(quit)

        tray.setContextMenu(main_menu)

        if with_server:
            self._spawn_server_on_thread()

        if testing_mode:
            self._launch_game_manager()

        self._gui_app.exec_()
