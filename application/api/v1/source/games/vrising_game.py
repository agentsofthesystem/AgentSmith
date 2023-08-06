import os
import subprocess

from jinja2 import Environment, FileSystemLoader
from multiprocessing import Process

from application.api.v1.source.models.games import Games
from application.api.v1.source.games.game_argument import GameArgument
from application.api.v1.source.games.game_base import BaseGame
from application.api.v1.source.games import utils
from application.common import logger, constants


class VrisingGame(BaseGame):
    def __init__(self) -> None:
        super(VrisingGame, self).__init__()

        self._game_name = "vrising"
        self._game_executable = "VRisingServer.exe"
        self._game_steam_id = "1829350"

        # Add Args here, can update later.
        self._add_argument(
            GameArgument("-persistentDataPath", value=None, required=True)
        )
        self._add_argument(
            GameArgument("-serverName", value=None, required=True, use_quotes=True)
        )
        self._add_argument(
            GameArgument("-saveName", value=None, required=True, use_quotes=True)
        )
        self._add_argument(
            GameArgument("-logFile", value=None, required=True, use_quotes=True)
        )

    def run_game(self, command, working_dir) -> None:
        subprocess.call(
            command,
            cwd=working_dir,
            creationflags=subprocess.DETACHED_PROCESS,  # Use this on windows-specifically.
            close_fds=True,
            # shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def startup(self) -> None:
        # Run base class checks
        super().startup()

        # Format command string.
        command = self._get_command_str()

        # Create a formatted batch file.
        env = Environment(loader=FileSystemLoader(utils.get_resources_dir()))
        template = env.get_template("start_server_template.bat.j2")
        output_from_parsed_template = template.render(
            GAME_STEAM_ID=self._game_steam_id,
            GAME_NAME=self._game_name,
            GAME_COMMAND=command,
        )

        # Print the formatted jinja
        logger.debug(output_from_parsed_template)

        # In theory, the software has already check that the game is installed, so no check/guard needed.
        game_obj = Games.query.filter_by(game_steam_id=self._game_steam_id).first()
        game_install_dir = game_obj.game_install_dir

        # Need game install locatoin to write batch file.
        full_path_startup_script = os.path.join(
            game_install_dir, constants.STARTUP_BATCH_FILE_NAME
        )

        # If file exists, remove it.
        if os.path.exists(full_path_startup_script):
            os.remove(full_path_startup_script)

        # Write the batch file.
        with open(full_path_startup_script, "w") as myfile:
            myfile.write(output_from_parsed_template)

        # Call the batch file on another process as to not block this one.
        p = Process(
            target=self.run_game,
            args=(
                full_path_startup_script,
                game_install_dir,
            ),
            name=self._game_name,
        )
        p.start()

        # p.pid
        # TODO - Store PID in database, so when a shutdown or or the app closes then it can be shutoff cleanly too.

    def shutdown(self) -> None:
        super().shutdown()
