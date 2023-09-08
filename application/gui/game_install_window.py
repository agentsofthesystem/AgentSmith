import requests
import sys

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QAction,
    QLayout,
)
from PyQt5.QtGui import QIcon

from application.gui.globals import GuiGlobals
from application.gui.widgets.new_game_widget import NewGameWidget


class GameInstallWindow(QMainWindow):
    def __init__(self, globals: GuiGlobals):
        super().__init__()
        self.title = "Game Installer"

        # TODO - Make these constants or compute middle of screen.
        self.left = 50
        self.top = 50
        self.width = 800
        self.height = 600

        self._initialized = False
        self._globals = globals
        self._new_game = NewGameWidget(self._globals, self)

    def init_ui(self):

        self.setWindowTitle(self.title)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(" &File")

        exitButton = QAction(QIcon("exit24.png"), " &Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self._new_game.init_ui()

        self.add_widget_items()

        self.setGeometry(self.left, self.top, self.width, self.height)

        self._initialized = True

    def add_widget_items(self):
        self._main_widget = QWidget(self)

        self._main_layout = QVBoxLayout()
        self._main_layout.sizeConstraint = QLayout.SetDefaultConstraint

        self._main_layout.addWidget(self._new_game)

        self._main_widget.setLayout(self._main_layout)

        self.setCentralWidget(self._main_widget)

        self.adjustSize()
        