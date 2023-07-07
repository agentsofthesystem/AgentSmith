import os
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
    def __init__(self, game_name: str, game_path: str) -> None:
        self._game_name = game_name
        self._game_path = game_path
        self._game_exe = self._game_path + os.sep + self._game_name

    def start_game(self, input_args=None) -> None:
        game_command = (self._game_exe, input_args)

        logger.info("*******************************************")
        logger.info(game_command)
        logger.info("*******************************************")

        return subprocess.run(game_command)

    def stop_game(self) -> None:
        pass
