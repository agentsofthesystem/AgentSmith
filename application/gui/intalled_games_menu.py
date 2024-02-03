import time

from PyQt5.QtWidgets import QMenu, QWidget, QWidgetAction, QPushButton

from application import games
from application.common import toolbox, logger
from application.common.decorators import timeit
from operator_client import Operator

BACKGROUND_STR = "background-color: {color}; padding: 8 8 8 8px;"
COLOR_RUNNING = "green"
COLOR_STOPPED = "red"


class InstalledGameMenu(QMenu):
    @timeit
    def __init__(self, parent: QWidget, client: Operator, init_data: dict) -> None:
        super(InstalledGameMenu, self).__init__("Quick Start/Stop", parent=parent)

        self._client = client
        self._parent = parent
        self._init_data = init_data
        self._buttons: dict = {}
        self._modules_dict = toolbox._find_conforming_modules(games)

        # Must call update_menu_list as opposed to update_menu to avoid overloading built in
        # function name!
        self.update_menu_list(initialize=True)

    @timeit
    def update_menu_list(self, initialize=False, delay_sec=0):
        if delay_sec > 0:
            time.sleep(delay_sec)

        self.clear()
        self._buttons.clear()

        if initialize:
            all_games = self._init_data
        else:
            all_games = self._client.game.get_games()
            all_games = all_games["items"]

        for game in all_games:
            game_name = game["game_name"]
            game_pretty_name = game["game_pretty_name"]
            game_pid = game["game_pid"]

            game_exe = self._get_executable_name(game_name)

            action = QWidgetAction(self)

            button = QPushButton(game_pretty_name)

            is_game_running = self._is_running(game_pid)
            is_exe_found = self._executable_is_found(game_exe)

            if is_game_running and is_exe_found:
                button.setStyleSheet(BACKGROUND_STR.format(color=COLOR_RUNNING))
            elif not is_game_running and is_exe_found:
                button.setStyleSheet(BACKGROUND_STR.format(color=COLOR_RUNNING))
            else:
                button.setStyleSheet(BACKGROUND_STR.format(color=COLOR_STOPPED))

            # There's a strange issue where passing arguments results in the same game name for any
            # button clicked.
            # This dict saves the game name, and the callback can look up info later.
            self._buttons[game_pretty_name] = game_name

            button.clicked.connect(self._handle_click)

            action.setDefaultWidget(button)

            self.addAction(action)

    def _is_running(self, game_pid):
        return True if game_pid else False

    def _get_executable_name(self, game_name) -> str:
        game_obj = None
        game_executable = ""

        for module_name in self._modules_dict.keys():
            game_obj = toolbox._instantiate_object(
                module_name, self._modules_dict[module_name]
            )
            if game_obj._game_name == game_name:
                game_executable = game_obj._game_executable

        return game_executable

    def _executable_is_found(self, exe_name: str) -> bool:
        return True if toolbox._get_proc_by_name(exe_name) else False

    def _handle_click(self):
        game_pretty_name = self.sender().text()

        game_name = self._buttons[game_pretty_name]

        # Getting the PID only means the game PID was once stored in the database.
        game_info = self._client.game.get_game_by_name(game_name)
        game_info = game_info["items"][0]
        game_pid = game_info["game_pid"]

        logger.debug(
            f"Installed Game Menu: Clicked on Game: {game_pretty_name}, Name: {game_name}, "
            f"PID: {game_pid}"
        )

        game_exe = self._get_executable_name(game_name)

        if self._is_running(game_pid) and self._executable_is_found(game_exe):
            # In this case, the game exe is found on the host, and the database is correct.
            self._client.game.game_shutdown(game_name)
        elif not self._is_running(game_pid) and self._executable_is_found(game_exe):
            # Catch the situation where the game pid in the DB is None/False, but the game exe is
            # still found on the host.
            self._client.game.game_shutdown(game_name)
        else:
            # Startup the game server on the host.
            args_list = self._client.game.get_argument_by_game_name(game_name)
            arg_dict = {}

            for arg in args_list:
                arg_dict[arg["game_arg"]] = arg["game_arg_value"]

            self._client.game.game_startup(game_name, input_args=arg_dict)

        self.update_menu_list(delay_sec=2)
