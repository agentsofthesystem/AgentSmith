import os
import platform
import psutil
import subprocess

from application.common import logger
from application.common import toolbox
from application.common.exceptions import GameManagerException
from pysteamcmd.steamcmd import Steamcmd


class SteamManager:
    def __init__(self, steam_install_dir) -> None:
        if not os.path.exists(steam_install_dir):
            os.makedirs(steam_install_dir, mode=0o777, exist_ok=True)

        toolbox.recursive_chmod(steam_install_dir)

        self._steam = Steamcmd(steam_install_dir)

        self._steam.install(force=True)

        toolbox.recursive_chmod(steam_install_dir)

        self._steamcmd_exe = self._steam.steamcmd_exe
        self._steam_install_dir = steam_install_dir

    def install_steam_app(
        self, steam_id, installation_dir, user="anonymous", password=None
    ):
        if not os.path.exists(installation_dir):
            os.makedirs(installation_dir, mode=0o777, exist_ok=True)

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

        # Need to add steamservice.so to the system path
        if self._steam.platform == "Linux":
            library_path = os.path.join(self._steam_install_dir, "linux64")
            update_environ = os.environ
            update_environ["LD_LIBRARY_PATH"] = library_path
            return subprocess.Popen(steamcmd_params, env=update_environ)
        else:
            # Otherwise, on windows, it's expected that steam is installed.
            return subprocess.Popen(steamcmd_params)


class GameManager:
    WIN_DETACHED_PROCESS = 8

    def __init__(self, game_name: str, game_path: str) -> None:
        self._game_name = game_name
        self._game_path = game_path
        self._game_exe = self._game_path + os.sep + self._game_name

        self._game_exe = os.path.join(self._game_path, self._game_name)

        self._platform = platform.system()

    @staticmethod
    def _print_command(list_list: list):
        output = ""
        for item in list_list:
            output += item + " "
        logger.info(output)

    def _get_proc_by_name(self, process_name: str):
        process = None

        current_procs = list((p for p in psutil.process_iter()))

        for proc in current_procs:
            proc_name = proc.name()

            if proc_name == "" or proc_name == " ":
                continue

            if proc_name == process_name:
                process = proc
                break

        return process

    def game_is_found(self, game_name: str) -> bool:
        return True if self._get_proc_by_name(game_name) else False

    def game_status(self, game_name: str):
        process_info = None
        process = self._get_proc_by_name(game_name)

        if process:
            process_info = process.as_dict()
            pass

        return process_info

    def start_game(self, input_args={}) -> None:
        """
        Start a game server with the input arguments provided, if any.

        Args:
            input_args (dict): Dictionary of key value pairs to use
            as inputs arguments.
        """
        if not os.path.exists(self._game_exe):
            raise GameManagerException(
                f"The game file does not exist: {self._game_exe}"
            )

        game_command = [self._game_exe]

        # TODO - Put a check that the game is not already running!

        if len(input_args.keys()) > 0:
            for arg in input_args:
                # TODO - This string format might not work for every game.
                game_command.append(f'{arg} "{input_args[arg]}"')

        # Get folder
        parent_folder = os.path.dirname(self._game_exe)

        if self._platform == "Windows":
            return subprocess.Popen(
                game_command,
                creationflags=self.WIN_DETACHED_PROCESS,  # Use this on windows-specifically.
                close_fds=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=parent_folder,
            )
        else:  # Linux
            game_command.append("&")
            self._print_command(game_command)
            return subprocess.Popen(
                game_command,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                cwd=parent_folder,
            )

    def stop_game(self, game_name: str) -> bool:
        is_process_stopped = False

        process = self._get_proc_by_name(game_name)

        if process:
            # is_process_stopped = True
            process.terminate()
            process.wait()
            is_process_stopped = True

        else:
            # process is None b/c it's not there... true in this case.
            is_process_stopped = True

        return is_process_stopped
