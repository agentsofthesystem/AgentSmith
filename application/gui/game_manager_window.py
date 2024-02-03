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
from application.gui.widgets.game_manager_widget import GameManagerWidget


class GameManagerWindow(QMainWindow):
    def __init__(self, globals: GuiGlobals):
        super().__init__()
        self.title = "Game Manager"

        self._initialized = False
        self._globals = globals
        self._game_manager_widget = GameManagerWidget(
            self._globals._client, globals, self
        )

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

        self._game_manager_widget.init_ui(all_games)

        self.add_widget_items()

        self._initialized = True

    def closeEvent(self, event):
        self._game_manager_widget.stop_timer()
        self._game_manager_widget.hide()

    def showWindow(self):
        # Wrapping the show method so the timer can be started, if it isn't already in
        # addition to calling show()

        self._game_manager_widget._disable_all_btns()

        self._game_manager_widget.start_timer(
            override_interval=self._game_manager_widget.FAST_INTERVAL
        )
        self._game_manager_widget.show()
        self.show()

    def add_widget_items(self):
        self._main_widget = QWidget(self)

        self._main_layout = QVBoxLayout()
        self._main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self._main_widget.setLayout(self._main_layout)

        self._main_layout.addWidget(self._game_manager_widget)

        self.setCentralWidget(self._main_widget)

        self.adjustSize()

    def update(self):
        self._game_manager_widget.update_installed_games()
