from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow,
    QAction,
    QTabWidget,
    QLayout,
)
from PyQt5.QtGui import QIcon

from application.gui.new_game_widget import NewGameWidget
from application.gui.game_summary_widget import GameSummaryWidget
from application.gui.settings_widget import SettingsWidget


class GameManagerWindow(QMainWindow):
    def __init__(self, globals):
        super().__init__()
        self.title = "Game Keeper Manager"

        # TODO - Make these constants or compute middle of screen.
        self.left = 50
        self.top = 50
        self.width = 1280
        self.height = 960

        self._initialized = False
        self._globals = globals
        self._new_game = NewGameWidget(self._globals._client, self)
        self._game_summary = GameSummaryWidget(self._globals._client, self)
        self._settings = SettingsWidget(self._globals._client, self._globals, self)

    def init_ui(self):
        self.setWindowTitle(self.title)

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.add_widget_items()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(" &File")

        updateButton = QAction(" &New Game", self)
        updateButton.setShortcut("Ctrl+N")
        updateButton.setStatusTip("Add a New Supported Game")
        updateButton.triggered.connect(self._show_new_game_widget)
        fileMenu.addAction(updateButton)

        exitButton = QAction(QIcon("exit24.png"), " &Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self._new_game.init_ui()
        self._game_summary.init_ui()

        self._initialized = True

    def add_widget_items(self):
        self._main_widget = QWidget(self)

        self._main_layout = QVBoxLayout()
        self._main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self._main_widget.setLayout(self._main_layout)

        self.tabs = QTabWidget()

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Reference
        # self.tab1_widget = NewGameWidget       self._new_game
        # self.tab2_widget = GameSummaryWidget   self._game_summary
        self.tab1.layout = QVBoxLayout()
        self.tab1.layout.addWidget(self._new_game)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QVBoxLayout()
        self.tab2.layout.addWidget(self._game_summary)
        self.tab2.setLayout(self.tab2.layout)

        self.tab3.layout = QVBoxLayout()
        self.tab3.layout.addWidget(self._settings)
        self.tab3.setLayout(self.tab3.layout)

        self.tabs.addTab(self.tab1, "New Game")
        self.tabs.addTab(self.tab2, "Game Summary")
        self.tabs.addTab(self.tab3, "Settings")

        self._main_layout.addWidget(self.tabs)

        self.setCentralWidget(self._main_widget)

    def _show_new_game_widget(self):
        if not self._new_game._initialized:
            self._new_game.init_ui()
        self._new_game.show()
