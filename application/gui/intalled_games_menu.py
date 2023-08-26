from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu, QWidget, QLabel, QWidgetAction

from client import Client

# Ref: https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html

GAME_IS_RUNNING = "QLabel { background-color : green; padding: 4 4 4 4px;}"
GAME_IS_STOPPED = "QLabel { background-color : red; padding: 4 4 4 4px;}"


class InstalledGameMenu(QMenu):
    def __init__(self, parent: QWidget, client: Client) -> None:
        super(InstalledGameMenu, self).__init__("Installed Games", parent=parent)

        self._client = client
        self._parent = parent
        self._game_running_icon = QIcon.fromTheme("face-cool")
        self._game_stopped_icon = QIcon.fromTheme("face-sad")

        self.update_menu()

    def update_menu(self):
        self.clear()

        all_games = self._client.game.get_games()
        all_games = all_games["items"]

        for game in all_games:
            game_name = game["game_name"]
            game_pretty_name = game["game_pretty_name"]
            game_pid = game["game_pid"]

            action = QWidgetAction(self._parent)

            label = QLabel(game_pretty_name)
            if self._is_running(game_pid):
                label.setStyleSheet(GAME_IS_RUNNING)
            else:
                label.setStyleSheet(GAME_IS_STOPPED)

            action.setDefaultWidget(label)
            action.triggered.connect(lambda: self.handle_click(game_pid, game_name))

            self.addAction(action)

    def _is_running(self, game_pid):
        return True if game_pid else False

    def handle_click(self, game_pid, game_name):
        # print(f"Button is clicked for game: {game_name}, Pid: {game_pid}")
        # print(type(game_pid))

        if self._is_running(game_pid):
            self._client.game.game_shutdown(game_name)
            self.setStyleSheet(GAME_IS_STOPPED)
        else:
            args_list = self._client.game.get_game_arguments(game_name)
            arg_dict = {}

            for arg in args_list:
                arg_dict[arg["game_arg"]] = arg["game_arg_value"]

            self._client.game.game_startup(game_name, input_args=arg_dict)
            self.setStyleSheet(GAME_IS_RUNNING)
