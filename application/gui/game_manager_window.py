import requests
import sys

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QAction,
    QLayout,
    QMessageBox,
)
from PyQt5.QtGui import QIcon

from application.gui.globals import GuiGlobals
from application.gui.widgets.game_control_widget import GameControlWidget


class GameManagerWindow(QMainWindow):
    def __init__(self, globals: GuiGlobals):
        super().__init__()
        self.title = "Game Manager"

        # TODO - Make these constants or compute middle of screen.
        self.left = 50
        self.top = 50
        self.width = 800
        self.height = 600

        self._initialized = False
        self._globals = globals
        self._game_control = GameControlWidget(self._globals._client, self)

    def init_ui(self):
        self.setWindowTitle(self.title)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(" &File")

        exitButton = QAction(QIcon("exit24.png"), " &Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Try to boil initialization down to the fewest API calls possible.
        try:
            game_data = self._globals._client.game.get_games()
            all_games = game_data["items"]
        except requests.exceptions.ConnectionError:
            message = QMessageBox()
            message.setText(
                "Error: Unable to start due to backend server being offline. Exiting..."
            )
            message.exec()
            sys.exit(1)

        self._game_control.init_ui(all_games)

        self.add_widget_items()

        self.setGeometry(self.left, self.top, self.width, self.height)

        self._initialized = True

    def add_widget_items(self):
        self._main_widget = QWidget(self)

        self._main_layout = QVBoxLayout()
        self._main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self._main_widget.setLayout(self._main_layout)

        self._main_layout.addWidget(self._game_control)

        self.setCentralWidget(self._main_widget)

        self.adjustSize()
