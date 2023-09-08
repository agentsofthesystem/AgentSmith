import requests

from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QVBoxLayout,
    QTableWidgetItem,
    QAbstractScrollArea,
    QLabel,
    QFrame,
    QComboBox
)
from PyQt5.QtCore import Qt

from application.common import constants, toolbox
from application.source import games
from client import Client


class GameControlWidget(QWidget):
    def __init__(self, client: Client, parent: QWidget) -> None:
        super().__init__(parent)

        self._parent = parent
        self._client = client
        self._layout = QVBoxLayout()
        self._installed_supported_games = {}
        self._current_game = None
        self._modules_dict = toolbox._find_conforming_modules(games)

    def _get_game_object(self, game_name):
        for module_name in self._modules_dict.keys():
            game_obj = toolbox._instantiate_object(
                module_name, self._modules_dict[module_name]
            )
            if game_obj._game_name == game_name:
                return game_obj
        return None

    def init_ui(self, game_data):

        self._layout.setAlignment(Qt.AlignTop)
        self._combo_box = QComboBox()      

        for game in game_data:
            game_pretty_name = game['game_pretty_name']
            game_name = game['game_name']
            game_obj = self._get_game_object(game_name)
            self._installed_supported_games[game_pretty_name] = game_obj
            self._combo_box.addItem(game_obj._game_pretty_name)

        self._combo_box.currentTextChanged.connect(self._text_changed)
        self._layout.addWidget(self._combo_box)

        # Separator
        h_sep = QFrame()
        h_sep.setFrameShape(QFrame.HLine)
        self._layout.addWidget(h_sep)

        # Get first game in supported games.
        installed_supported_games = list(self._installed_supported_games.keys())
        self._current_game = self._build_game_frame(installed_supported_games[0])
        self._layout.addWidget(self._current_game)

        self.setLayout(self._layout)

        self.show()

        self._initialized = True

    def _build_game_frame(self, game_name):
        game_frame = QFrame()
        v_layout = QVBoxLayout()
        label = QLabel(f"Game is: {game_name}")
        v_layout.addWidget(label)
        
        #game_object = self._supported_games[game_name]

        game_frame.setLayout(v_layout)
        game_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        game_frame.setLineWidth(1)

        return game_frame

    def _text_changed(self, game_pretty_name):
        print("Curent Game changed to:", game_pretty_name)
        old_game = self._current_game
        old_game.hide()
        self._current_args_list = []
        self._current_game = self._build_game_frame(game_pretty_name)
        self._layout.replaceWidget(old_game, self._current_game)