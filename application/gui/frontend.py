import os

from PyQt5.QtWidgets import QAction, QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon

from application.gui.globals import GuiGlobals


class GuiApp:
    def __init__(self) -> None:
        self._globals = GuiGlobals()

    def initialize(self):
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

        # Adding an icon
        current_file = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_file)
        icon_path = os.path.join(current_folder, "resources", "keeper.png")
        icon = QIcon(icon_path)

        # Adding item on the menu bar
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        # Creating the options
        menu = QMenu()
        option1 = QAction("Games")
        menu.addAction(option1)

        # To quit the app
        quit = QAction("Quit")
        quit.triggered.connect(app.quit)
        menu.addAction(quit)

        # Adding options to the System Tray
        tray.setContextMenu(menu)

        app.exec_()
