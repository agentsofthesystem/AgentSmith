import requests

from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QVBoxLayout,
    QTableWidgetItem,
    QAbstractScrollArea,
)

from client import Client


class GameSummaryWidget(QWidget):
    def __init__(self, client: Client, parent: QWidget) -> None:
        super().__init__(parent)

        self._parent = parent
        self._client = client
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
        self.game_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.layout.addWidget(self.game_table)

        self.setLayout(self.layout)

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

        self._parent.adjustSize()
