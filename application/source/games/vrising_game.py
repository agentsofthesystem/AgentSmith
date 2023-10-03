import os
import subprocess
import time

from jinja2 import Environment, FileSystemLoader

from application.common import logger, constants
from application.common.game_argument import GameArgument
from application.common.game_base import BaseGame
from application.common.toolbox import _get_proc_by_name, get_resources_dir
from application.extensions import DATABASE
from application.source.models.games import Games


class VrisingGame(BaseGame):
    def __init__(self) -> None:
        super(VrisingGame, self).__init__()

        self._game_name = "vrising"
        self._game_pretty_name = "V Rising"
        self._game_executable = "VRisingServer.exe"
        self._game_steam_id = "1829350"
        self._game_info_url = (
            "https://github.com/StunlockStudios/vrising-dedicated-server-instructions"
        )

        # Add Args here, can update later.
        self._add_argument(
            GameArgument(
                "-persistentDataPath",
                value=None,
                required=True,
                is_permanent=True,
                file_mode=constants.FileModes.DIRECTORY.value,
            )
        )
        self._add_argument(
            GameArgument(
                "-serverName",
                value=None,
                required=True,
                use_quotes=True,
                is_permanent=True,
            )
        )
        self._add_argument(
            GameArgument(
                "-saveName",
                value=None,
                required=True,
                use_quotes=True,
                is_permanent=True,
            )
        )
        self._add_argument(
            GameArgument(
                "-logFile",
                value=None,
                required=True,
                use_quotes=True,
                is_permanent=True,
                file_mode=constants.FileModes.FILE.value,
            )
        )
        # Default is 27015
        self._add_argument(
            GameArgument(
                "-serverPort",
                value=27015,
                required=True,
                use_quotes=True,
                is_permanent=True,
            )
        )

    def _run_game(self, command, working_dir) -> None:
        return subprocess.call(
            command,
            cwd=working_dir,
            creationflags=subprocess.DETACHED_PROCESS,  # Use this on windows-specifically.
            close_fds=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def startup(self) -> None:
        # Run base class checks
        super().startup()

        # Format command string.
        command = self._get_command_str()

        # Create a formatted batch file.
        env = Environment(
            loader=FileSystemLoader(get_resources_dir(__file__))
        )  # TODO - pyinstaller will change this.
        template = env.get_template("start_server_template.bat.j2")
        output_from_parsed_template = template.render(
            GAME_STEAM_ID=self._game_steam_id,
            GAME_NAME=self._game_name,
            GAME_COMMAND=command,
        )

        # Print the formatted jinja
        logger.debug(output_from_parsed_template)

        # In theory, the software has already check that the game is installed, so no check/guard needed.
        game_qry = Games.query.filter_by(game_steam_id=self._game_steam_id)
        game_obj = game_qry.first()
        game_install_dir = game_obj.game_install_dir

        # Need game install location to write batch file.
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
        command = f'START /MIN CMD.EXE /C "{full_path_startup_script}"'
        result = self._run_game(command, game_install_dir)

        time.sleep(1)

        process = _get_proc_by_name(self._game_executable)

        logger.info(result)
        logger.info("Process:")
        logger.info(process)

        update_dict = {"game_pid": int(process.pid)}

        game_qry.update(update_dict)
        DATABASE.session.commit()

    def shutdown(self) -> None:
        game_qry = Games.query.filter_by(game_steam_id=self._game_steam_id)
        game_obj = game_qry.first()
        game_pid = game_obj.game_pid

        process = _get_proc_by_name(self._game_executable)

        if process:
            logger.info(process)
            logger.info(game_pid)

            process.terminate()
            process.wait()

            update_dict = {"game_pid": None}
            game_qry.update(update_dict)
            DATABASE.session.commit()
