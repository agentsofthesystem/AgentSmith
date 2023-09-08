import requests
import sys

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QAction,
    QTabWidget,
    QLayout,
    QMessageBox,
)
from PyQt5.QtGui import QIcon

from application.gui.globals import GuiGlobals
from application.gui.widgets.game_control_widget import GameControlWidget
from application.gui.widgets.game_summary_widget import GameSummaryWidget
from application.gui.widgets.settings_widget import SettingsWidget


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
        self._game_summary = GameSummaryWidget(self._globals._client, self)
        self._settings = SettingsWidget(self._globals._client, self._globals, self)

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
        self._game_summary.init_ui(all_games)
        self._settings.init_ui()

        self.add_widget_items()

        self.setGeometry(self.left, self.top, self.width, self.height)

        self._initialized = True

    def _add_tab_widget(self, title: str, widget: QWidget):

        tab = QWidget()
        tab.layout = QVBoxLayout()
        tab.layout.addWidget(widget)
        tab.setLayout(tab.layout)

        self.tabs.addTab(tab, title)

    def add_widget_items(self):
        self._main_widget = QWidget(self)

        self._main_layout = QVBoxLayout()
        self._main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self._main_widget.setLayout(self._main_layout)

        self.tabs = QTabWidget()
        self.tabs.setUsesScrollButtons(False)
        self.tabs.currentChanged.connect(self._on_tab_change)  # changed!

        tab_items = [
            ("Game Control", self._game_control),
            ("Game Summary", self._game_summary),
            ("Settings", self._settings)
        ]

        for tab in tab_items:
            self._add_tab_widget(tab[0], tab[1])

        self._main_layout.addWidget(self.tabs)

        self.setCentralWidget(self._main_widget)

        self.adjustSize()

    def _on_tab_change(self):
        self._game_summary.update_table()
