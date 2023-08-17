import requests

from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow,
    QAction,
    QLayout,
    QTableWidgetItem,
)
from PyQt5.QtGui import QIcon

from client import Client

# Reference: https://github.com/jreed1701/PyQt-Stock-Watchlist/blob/master/source/watchlist_table_widget.py


class AllGamesTableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "All Games Table"

        # TODO - Make these constants or compute middle of screen.
        self.left = 50
        self.top = 50
        self.width = 1280
        self.height = 960

        self._initialized = False
        self._table_widget = AllGamesTableWidget(self)

    def init_ui(self):
        self.setWindowTitle(self.title)

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.add_widget_items()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(" &File")

        exitButton = QAction(QIcon("exit24.png"), " &Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self._table_widget.init_ui()
        self._initialized = True

    def add_widget_items(self):
        self._main_widget = QWidget(self)

        self._main_layout = QHBoxLayout(self._main_widget)
        self._main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self._main_layout.addWidget(self._table_widget)

        self._main_widget.setLayout(self._main_layout)
        self.setCentralWidget(self._main_widget)


class AllGamesTableWidget(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self._client = Client("http://localhost", 3000, verbose=False)

        self._num_cols = 0

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.game_table = QTableWidget()

        # Get schema from server and populate labesl and column count.
        # TODO - Make the backend serve up "pretty names"
        # try:
        try:
            cols = self._client.game.get_games_schema()
        except requests.exceptions.ConnectionError:
            cols = ["ERROR"]

        self._num_cols = len(cols)
        self.game_table.setColumnCount(self._num_cols)
        self.game_table.setHorizontalHeaderLabels(cols)

        self.layout.addWidget(self.game_table)

        self.setLayout(self.layout)

        self.update_table()

    def update_table(self):
        try:
            game_data = self._client.game.get_games()
            all_games = game_data["items"]
        except requests.exceptions.ConnectionError:
            all_games = [{"ERROR": "Connection Error"}]

        num_rows = len(all_games)
        self.game_table.setRowCount(num_rows)

        for r in range(0, num_rows):
            current_game = all_games[r]  # dict
            column = 0

            for _, value in current_game.items():
                self.game_table.setItem(r, column, QTableWidgetItem(str(value)))
                column += 1

        self.game_table.resizeColumnsToContents()
