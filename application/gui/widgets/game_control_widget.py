from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QComboBox,
    QHBoxLayout,
    QLayout,
)
from PyQt5.QtCore import Qt

from application.common import toolbox
from application.common.game_base import BaseGame
from application.source import games
from application.gui.widgets.game_arguments_widget import GameArgumentsWidget
from client import Client


class GameControlWidget(QWidget):
    def __init__(self, client: Client, parent: QWidget) -> None:
        super(QWidget, self).__init__(parent)

        self._parent = parent
        self._client = client

        self._layout = QVBoxLayout()
        self._combo_box = QComboBox()
        self._layout.sizeConstraint = QLayout.SetDefaultConstraint

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
        if len(self._installed_supported_games.keys()) == 0:
            self.update_installed_games()

        print(game_name)

        game_object: BaseGame = self._installed_supported_games[game_name]

        game_frame = QFrame()
        game_frame.sizeConstraint = QLayout.SetDefaultConstraint

        # Main layout box
        game_frame_main_layout = QVBoxLayout()

        # Static Game Information
        game_info_label = QLabel("Game Information:", game_frame)
        game_info_label.setStyleSheet("text-decoration: underline;")
        game_frame_main_layout.addWidget(game_info_label)

        h_layout_all_game_info = QHBoxLayout()
        v_layout_info_labels = QVBoxLayout()
        v_layout_info_info_text = QVBoxLayout()

        v_layout_info_labels.addWidget(QLabel("Game Pretty Name", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Exe Name", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Steam ID", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Info URL", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game PID", game_frame))
        v_layout_info_labels.addWidget(QLabel("Game Exe Found?", game_frame))

        v_layout_info_info_text.addWidget(
            QLabel(game_object._game_pretty_name, game_frame)
        )
        v_layout_info_info_text.addWidget(
            QLabel(game_object._game_executable, game_frame)
        )
        v_layout_info_info_text.addWidget(
            QLabel(game_object._game_steam_id, game_frame)
        )
        v_layout_info_info_text.addWidget(QLabel("NOT YET IMPLEMENTED", game_frame))
        v_layout_info_info_text.addWidget(QLabel("NOT YET IMPLEMENTED", game_frame))

        url_link = (
            f'<a href="{game_object._game_info_url}"> {game_object._game_info_url}</a>'
        )
        game_info_url = QLabel(url_link, game_frame)
        game_info_url.setOpenExternalLinks(True)
        v_layout_info_info_text.addWidget(game_info_url)

        h_layout_all_game_info.addLayout(v_layout_info_labels)
        h_layout_all_game_info.addLayout(v_layout_info_info_text)
        game_frame_main_layout.addLayout(h_layout_all_game_info)

        # Game Arguments

        game_args_label = QLabel("Game Arguments:", game_frame)
        game_args_label.setStyleSheet("text-decoration: underline;")
        game_args = self._client.game.get_argument_by_game_name(game_object._game_name)
        arg_widget = GameArgumentsWidget(self._client, game_args, game_frame)

        game_frame_main_layout.addWidget(game_args_label)
        game_frame_main_layout.addWidget(arg_widget)
        game_frame_main_layout.addWidget(QPushButton("Add Argument"))

        # Game controls
        game_control_label = QLabel("Game Controls:", game_frame)
        game_control_label.setStyleSheet("text-decoration: underline;")
        game_frame_main_layout.addWidget(game_control_label)

        game_control_h_layout = QHBoxLayout()

        game_control_h_layout.addWidget(QPushButton("Startup"))
        game_control_h_layout.addWidget(QPushButton("Shutdown"))
        game_control_h_layout.addWidget(QPushButton("Restart"))
        game_control_h_layout.addWidget(QPushButton("Uninstall"))
        game_frame_main_layout.addLayout(game_control_h_layout)

        # Finalize game frame
        game_frame.setLayout(game_frame_main_layout)
        game_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        game_frame.setLineWidth(1)
        game_frame.adjustSize()

        return game_frame

    def _text_changed(self, game_pretty_name):
        print("Curent Game changed to:", game_pretty_name)

        if game_pretty_name == "":
            return

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
