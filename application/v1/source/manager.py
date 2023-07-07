import os
import psutil
import subprocess

from application.common import logger
from pysteamcmd.steamcmd import Steamcmd


class SteamManager:
    def __init__(self, steam_install_dir) -> None:
        self._steam = Steamcmd(steam_install_dir)

        self._steam.install(force=True)

        self._steamcmd_exe = self._steam.steamcmd_exe

    def install_steam_app(
        self, steam_id, installation_dir, user="anonymous", password=None
    ):
        return self._install_gamefiles(
            gameid=steam_id,
            game_install_dir=installation_dir,
            user=user,
            password=password,
            validate=True,
        )

    def _install_gamefiles(
        self, gameid, game_install_dir, user="anonymous", password=None, validate=False
    ):
        """
        Installs gamefiles for dedicated server. This can also be used to update the gameserver.
        :param gameid: steam game id for the files downloaded
        :param game_install_dir: installation directory for gameserver files
        :param user: steam username (defaults anonymous)
        :param password: steam password (defaults None)
        :param validate: should steamcmd validate the gameserver files (takes a while)
        :return: subprocess call to steamcmd
        """
        if validate:
            validate = "validate"
        else:
            validate = None

        steamcmd_params = (
            self._steamcmd_exe,
            "+login {} {}".format(user, password),
            "+force_install_dir {}".format(game_install_dir),
            "+app_update {}".format(gameid),
            "{}".format(validate),
            "+quit",
        )

        return subprocess.run(steamcmd_params)


class GameManager:
    WIN_DETACHED_PROCESS = 8

    def __init__(self, game_name: str, game_path: str) -> None:
        self._game_name = game_name
        self._game_path = game_path
        self._game_exe = self._game_path + os.sep + self._game_name

    def check_game(self, game_name: str) -> bool:
        is_running = False

        if game_name in (p.name() for p in psutil.process_iter()):
            is_running = True

        return is_running

    def start_game(self, input_args={}) -> None:
        game_command = [self._game_exe]

        # TODO - Put a check that the game is not already running!

        if len(input_args.keys()) > 0:
            for arg in input_args:
                # TODO - This might not work for every game.
                game_command.append(f'{arg} "{input_args[arg]}"')

        return subprocess.Popen(
            game_command, creationflags=self.WIN_DETACHED_PROCESS, close_fds=True
        )

    def stop_game(self) -> None:
        pass
