from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QVBoxLayout,
    QTableWidgetItem,
    QAbstractScrollArea,
    QLabel,
    QFrame,
    QComboBox,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt

from application.common import toolbox
from application.source import games
from application.gui.widgets.game_arguments_widget import GameArgumentsWidget
from client import Client


class GameControlWidget(QWidget):
    def __init__(self, client: Client, parent: QWidget) -> None:
        super().__init__(parent)

        self._parent = parent
        self._client = client
        self._layout = QVBoxLayout()
        self._installed_supported_games = {}
        self._current_game_frame = None
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
        self._layout.addWidget(self._combo_box)

        # Separator
        h_sep = QFrame()
        h_sep.setFrameShape(QFrame.HLine)
        self._layout.addWidget(h_sep)

        # Get first game in supported games.
        self.update_installed_games(game_data=game_data)

        self._combo_box.currentTextChanged.connect(self._text_changed)

        self.setLayout(self._layout)

        self.show()

        self._initialized = True

    def update_installed_games(self, game_data=None):
        if game_data is None:
            game_data = self._client.game.get_games()
            game_data = game_data["items"]

        self._combo_box.clear()
        self._installed_supported_games.clear()

        for game in game_data:
            game_pretty_name = game["game_pretty_name"]
            game_name = game["game_name"]
            game_obj = self._get_game_object(game_name)
            self._installed_supported_games[game_pretty_name] = game_obj
            self._combo_box.addItem(game_obj._game_pretty_name)

        installed_supported_games = list(self._installed_supported_games.keys())

        if len(installed_supported_games) > 0:
            self._current_game_frame = self._build_game_frame(
                installed_supported_games[0]
            )
            self._layout.addWidget(self._current_game_frame)

    def _build_game_frame(self, game_name):
        game_object = self._installed_supported_games[game_name]

        game_frame = QFrame()

        v_layout = QVBoxLayout()

        # Game Info

        # Separate game info from game arguments
        h_sep = QFrame()
        h_sep.setFrameShape(QFrame.HLine)
        v_layout.addWidget(h_sep)

        title1 = QLabel("Game Information:")
        title1.setStyleSheet("text-decoration: underline")
        v_layout.addWidget(title1)

        h_layout_all_game_info = QHBoxLayout()
        v_layout_info_labels = QVBoxLayout()
        v_layout_info_info_text = QVBoxLayout()

        v_layout_info_labels.addWidget(QLabel("Game Pretty Name"))
        v_layout_info_labels.addWidget(QLabel("Game Exe Name"))
        v_layout_info_labels.addWidget(QLabel("Game Steam ID"))
        v_layout_info_labels.addWidget(QLabel("Game Infor URL"))

        v_layout_info_info_text.addWidget(QLabel(game_object._game_pretty_name))
        v_layout_info_info_text.addWidget(QLabel(game_object._game_executable))
        v_layout_info_info_text.addWidget(QLabel(game_object._game_steam_id))

        url_link = (
            f'<a href="{game_object._game_info_url}"> {game_object._game_info_url}</a>'
        )
        game_info_url = QLabel(url_link)
        game_info_url.setOpenExternalLinks(True)
        v_layout_info_info_text.addWidget(game_info_url)

        h_layout_all_game_info.addLayout(v_layout_info_labels)
        h_layout_all_game_info.addLayout(v_layout_info_info_text)

        v_layout.addLayout(h_layout_all_game_info)

        # Game Arguments
        title2 = QLabel("Game Arguments:")
        title2.setStyleSheet("text-decoration: underline")
        v_layout.addWidget(title2)

        game_args = self._client.game.get_argument_by_game_name(game_object._game_name)
        arg_widget = GameArgumentsWidget(self._client, game_args, self)
        v_layout.addWidget(arg_widget)

        # Game Arguments
        title3 = QLabel("Game Commands:")
        title3.setStyleSheet("text-decoration: underline")
        v_layout.addWidget(title3)

        v_layout.addWidget(h_sep)

        game_frame.setLayout(v_layout)
        game_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        game_frame.setLineWidth(1)

        return game_frame

    def _text_changed(self, game_pretty_name):
        print("Curent Game changed to:", game_pretty_name)

        self._current_args_list = []
        self._current_game_frame = self._build_game_frame(game_pretty_name)

        # This callback might be triggered in the situation where there never was a current game. Ie. The first
        # game being installed.
        if self._current_game_frame is None:
            self._layout.addWidget(self._current_game_frame)
        else:
            old_game_frame = self._current_game_frame
            old_game_frame.hide()
            self._layout.replaceWidget(old_game_frame, self._current_game_frame)
