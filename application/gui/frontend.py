import os

from flask import Flask
from threading import Thread
from PyQt5.QtWidgets import QAction, QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon

from application.config.config import DefaultConfig
from application.gui.globals import GuiGlobals
from application.factory import create_app


class GuiApp:
    def __init__(self, globals_obj: GuiGlobals) -> None:
        self._globals = globals_obj
        self._globals._FLASK_APP = self._create_backend()
        self._gui_app = None
        self._server_thread = None

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

    def _test_func(self):
        print("Test Function!")

    def initialize(self, with_server=False):
        self._gui_app = QApplication([])
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
        menu = QMenu()
        option1 = QAction("Games")
        option1.triggered.connect(self._test_func)
        menu.addAction(option1)

        # To quit the app
        quit = QAction("Quit")
        quit.triggered.connect(self.quit_gui)
        menu.addAction(quit)

        # Adding options to the System Tray
        tray.setContextMenu(menu)

        if with_server:
            self._spawn_server_on_thread()

        self._gui_app.exec_()
