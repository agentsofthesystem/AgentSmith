import os
import time

from jinja2 import Environment, FileSystemLoader

from application.common import logger, constants
from application.common.game_argument import GameArgument
from application.common.game_base import BaseGame
from application.common.toolbox import _get_proc_by_name, get_resources_dir
from application.extensions import DATABASE
from application.models.games import Games


class VrisingGame(BaseGame):
    def __init__(self, defaults_dict: dict = {}) -> None:
        super(VrisingGame, self).__init__(defaults_dict)

        self._game_name = "valheim"
        self._game_pretty_name = "Valheim"
        self._game_executable = "valheim_server.exe"
        self._game_steam_id = "896660"
        self._game_info_url = (
            "https://valheim.com/support/a-guide-to-dedicated-servers/"
        )

        if self._game_default_install_dir:
            default_persistent_data_path = os.path.join(
                self._game_default_install_dir,
                constants.GAME_INSTALL_FOLDER,
                self._game_name,
                "saves",
            )
            default_log_path = os.path.join(
                self._game_default_install_dir,
                constants.GAME_INSTALL_FOLDER,
                self._game_name,
                "logs",
                "valheim.txt",
            )
        else:
            default_persistent_data_path = None
            default_log_path = None

        # Add Args here, can update later.
        # Default is 2456
        self._add_argument(
            GameArgument(
                "-name",
                value="Valheim",
                required=True,
                use_quotes=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-port",
                value=2456,
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-world",
                value="badlands",
                required=True,
                use_quotes=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-password",
                value="abc123",
                required=True,
                use_quotes=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-savedir",
                value=default_persistent_data_path,
                required=True,
                use_quotes=True,
                is_permanent=True,
                file_mode=constants.FileModes.DIRECTORY.value,
            )
        )

        self._add_argument(
            GameArgument(
                "-public",
                value="0",
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-logFile",
                value=default_log_path,
                required=True,
                use_quotes=True,
                is_permanent=True,
                file_mode=constants.FileModes.FILE.value,
            )
        )

        self._add_argument(
            GameArgument(
                "-saveinterval",
                value="1800",
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-backups",
                value="4",
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-backupshort",
                value="7200",
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-backuplong",
                value="43200",
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-crossplay",
                value=" ",
                required=True,
                use_quotes=False,
                is_permanent=False,
            )
        )

        self._add_argument(
            GameArgument(
                "-preset",
                value="normal",
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

    def startup(self) -> None:
        # Run base class checks
        super().startup()

        # Format command string.
        command_args = self._get_command_str(args_only=True)

        # Create a formatted batch file.
        env = Environment(loader=FileSystemLoader(get_resources_dir(__file__)))
        template = env.get_template("start_valheim_server_template.bat.j2")
        output_from_parsed_template = template.render(
            GAME_STEAM_ID=self._game_steam_id,
            GAME_NAME=self._game_name,
            GAME_ARGUMENTS=command_args,
        )

        # Print the formatted jinja
        logger.debug(output_from_parsed_template)

        # In theory, the software has already check that the game is installed, so no check/guard
        # needed.
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
