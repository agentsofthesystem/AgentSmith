import os
import time

from jinja2 import Environment, FileSystemLoader

from application.common import logger, constants
from application.common.game_argument import GameArgument
from application.common.game_base import BaseGame
from application.common.toolbox import _get_proc_by_name, get_resources_dir
from application.extensions import DATABASE
from application.models.games import Games


class Satisfactory(BaseGame):
    def __init__(self, defaults_dict: dict = {}) -> None:
        super(Satisfactory, self).__init__(defaults_dict)

        self._game_name = "satisfactory"
        self._game_pretty_name = "Satisfactory"
        self._game_executable = "FactoryServer.exe"
        self._game_steam_id = "1690800"
        self._game_info_url = "https://satisfactory.fandom.com/wiki/Dedicated_servers"

        # Add Args here, can update later.
        # Default is 2456
        self._add_argument(
            GameArgument(
                "-multihome",
                value="0.0.0.0",
                required=True,
                use_quotes=False,
                use_equals=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-Port",
                value=15002,
                required=True,
                use_quotes=False,
                use_equals=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-ServerQueryPort",
                value=15000,
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-BeaconPort",
                value=15001,
                required=True,
                use_quotes=False,
                use_equals=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "-log",
                value=" ",
                required=False,
                use_quotes=False,
                is_permanent=False,
            )
        )

        self._add_argument(
            GameArgument(
                "-unattended",
                value=" ",
                required=False,
                use_quotes=False,
                is_permanent=False,
            )
        )

        self._add_argument(
            GameArgument(
                "-DisablePacketRouting",
                value=" ",
                required=False,
                use_quotes=False,
                is_permanent=False,
            )
        )

    def startup(self) -> None:
        # Run base class checks
        super().startup()

        # Format command string.
        command = self._get_command_str(args_only=False)

        # Create a formatted batch file.
        env = Environment(loader=FileSystemLoader(get_resources_dir(__file__)))
        template = env.get_template("start_satisfactory_server_template.bat.j2")
        output_from_parsed_template = template.render(
            GAME_STEAM_ID=self._game_steam_id,
            GAME_NAME=self._game_name,
            GAME_COMMAND=command,
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

        process_2 = _get_proc_by_name("UnrealServer-Win64-Shipping.exe")

        if process:
            logger.info(process_2)
            process_2.terminate()
            process_2.wait()
