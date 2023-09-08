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

    def _populate_table(self, all_games):
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

    def init_ui(self, game_data):
        self.layout = QVBoxLayout()

        self.game_table = QTableWidget()
        all_games = game_data

        # Get columns from all game data on init. On init, it's possible no games are installed yet,
        # so if that happens, just get the schema.
        if len(all_games) > 0:
            first_game = all_games[0].keys()
            cols = [game for game in first_game]
        else:
            all_games = [{"Warning": "No Games Installed"}]
            cols = self._client.game.get_games_schema()

        self._num_cols = len(cols)
        self.game_table.setColumnCount(self._num_cols)
        self.game_table.setHorizontalHeaderLabels(cols)
        self.game_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self._populate_table(game_data)

        self.layout.addWidget(self.game_table)

        self.setLayout(self.layout)

    def update_table(self):
        try:
            game_data = self._client.game.get_games()
            all_games = game_data["items"]
        except requests.exceptions.ConnectionError:
            all_games = [{"ERROR": "Connection Error"}]

        self._populate_table(all_games)
