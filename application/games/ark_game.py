import os
import time

from jinja2 import Environment, FileSystemLoader

from application.common import logger, constants
from application.common.game_argument import GameArgument
from application.common.game_base import BaseGame
from application.common.toolbox import _get_proc_by_name, get_resources_dir
from application.extensions import DATABASE
from application.models.games import Games


class ArkGame(BaseGame):
    def __init__(self, defaults_dict: dict = {}) -> None:
        super(ArkGame, self).__init__(defaults_dict)

        self._game_name = "ark"
        self._game_pretty_name = "Ark: Survival Evolved"
        self._game_executable = "ShooterGameServer.exe"
        self._game_steam_id = "376030"
        self._game_info_url = "https://ark.fandom.com/wiki/Dedicated_server_setup"

        """
        Reference:

        start ShooterGameServer.exe TheIsland?listen?SessionName=<server_name>
        ?ServerPassword=<join_password>
        ?ServerAdminPassword=<admin_password>?Port=<port>
        ?QueryPort=<query_port>?MaxPlayers=<max_players>
        exit
        """

        # Add Args here, can update later.
        self._add_argument(
            GameArgument(
                "server_name",
                value="MyArkServer",
                required=True,
                use_quotes=False,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "join_password",
                value="abc123",
                required=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "admin_password",
                value="abc123",
                required=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "port",
                value=7777,
                required=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "query_port",
                value=27015,
                required=True,
                is_permanent=True,
            )
        )

        self._add_argument(
            GameArgument(
                "max_players",
                value=4,
                required=True,
                is_permanent=True,
            )
        )

    def startup(self) -> None:
        # Run base class checks
        super().startup()

        # Get individual arguments for this game
        arguments = self._get_argument_dict()

        server_name = arguments["server_name"]._value
        join_password = arguments["join_password"]._value
        admin_password = arguments["admin_password"]._value
        port = arguments["port"]._value
        query_port = arguments["query_port"]._value
        max_players = arguments["max_players"]._value

        # Create a formatted batch file.
        env = Environment(loader=FileSystemLoader(get_resources_dir(__file__)))
        template = env.get_template("start_ark_server_template.bat.j2")
        output_from_parsed_template = template.render(
            GAME_STEAM_ID=self._game_steam_id,
            GAME_NAME=self._game_name,
            server_name=server_name,
            join_password=join_password,
            admin_password=admin_password,
            port=port,
            query_port=query_port,
            max_players=max_players,
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

        game_working_dir = os.path.join(
            game_install_dir, "ShooterGame", "Binaries", "Win64"
        )

        # If file exists, remove it.
        if os.path.exists(full_path_startup_script):
            os.remove(full_path_startup_script)

        # Write the batch file.
        with open(full_path_startup_script, "w") as myfile:
            myfile.write(output_from_parsed_template)

        # Call the batch file on another process as to not block this one.
        command = f'START /MIN CMD.EXE /C "{full_path_startup_script}"'
        result = self._run_game(command, game_working_dir)

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
