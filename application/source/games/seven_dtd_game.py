import os
import time
import xml.etree.ElementTree as ET

from jinja2 import Environment, FileSystemLoader
from telnetlib import Telnet

from application.common import logger, constants
from application.common.game_argument import GameArgument
from application.common.game_base import BaseGame
from application.common.toolbox import _get_proc_by_name, get_resources_dir
from application.extensions import DATABASE
from application.source.models.games import Games

# NOTE - This Game is not yet implemented.


class SevenDaysToDieGame(BaseGame):
    def __init__(self) -> None:
        super(SevenDaysToDieGame, self).__init__()

        self._game_name = "7dtd"
        self._game_pretty_name = "7 Days To Die"
        self._game_executable = "7DaysToDieServer.exe"
        self._game_steam_id = "294420"
        self._game_info_url = (
            "https://developer.valvesoftware.com/wiki/7_Days_to_Die_Dedicated_Server"
        )

        self._telnet = Telnet()

        # Add Args here, can update later.
        self._add_argument(
            GameArgument(
                "LogFileName", value="output_log", required=True, is_permanent=True
            )
        )
        self._add_argument(
            GameArgument(
                "ServerConfigFilePath",
                value=None,
                required=True,
                is_permanent=True,
                file_mode=constants.FileModes.FILE.value,
            )
        )

    def startup(self) -> None:
        # Run base class checks
        # Run base class checks
        super().startup()

        # In theory, the software has already check that the game is installed, so no check/guard needed.
        game_qry = Games.query.filter_by(game_steam_id=self._game_steam_id)
        game_obj = game_qry.first()
        game_install_dir = game_obj.game_install_dir

        # Format command string.
        arguments = self._get_argument_dict()
        log_file_name = arguments["LogFileName"]._value
        config_file_full_path = arguments["ServerConfigFilePath"]._value
        config_file_full_path = config_file_full_path.replace("/", "\\")

        # Create a formatted batch file.
        env = Environment(loader=FileSystemLoader(get_resources_dir(__file__)))
        template = env.get_template("start_7dtd_server_template.bat.j2")
        output_from_parsed_template = template.render(
            LOG_FILE_NAME=log_file_name,
            CONFIG_FILE_FULL_PATH=config_file_full_path,
        )

        # Print the formatted jinja
        logger.debug(output_from_parsed_template)

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

        time.sleep(10)

        process = _get_proc_by_name(self._game_executable)

        logger.info(result)
        logger.info("Process:")
        logger.info(process)

        if process:
            update_dict = {"game_pid": int(process.pid)}
            game_qry.update(update_dict)
            DATABASE.session.commit()
        else:
            logger.critical(
                f"7Days To Die: {self._game_executable} not found on server."
            )

    def shutdown(self) -> None:
        """
        Shutdown 7DTD server using telnet interface.  Why telnet? The issue is because simply
        finding the exe and killing the process will result in the 7dtd corrupting game files.
        It's not a clean exit.  This works for some games but not this one.
        """

        # Telnet client command is simply "shutdown"; default telnet port is localhost:8081
        # telnet client is built in to python.
        # In theory, the software has already check that the game is installed, so no check/guard needed.
        game_qry = Games.query.filter_by(game_steam_id=self._game_steam_id)

        # This refreshes the argument dictionary with the config file path in the database.
        self._rebuild_arguments_dict()

        # Format command string.
        arguments = self._get_argument_dict()
        config_file_full_path = arguments["ServerConfigFilePath"]._value

        tree = ET.parse(config_file_full_path)
        root = tree.getroot()

        telnet_port = None
        telnet_pass = ""  # assume no pass

        for property in root.iter("property"):
            name = property.get("name")
            if name == "TelnetPort":
                telnet_port = property.get("value")
            if name == "TelnetPassword":
                telnet_pass = property.get("value")

        if telnet_port is None:
            logger.critical(
                "7Days To Die: ERROR... cannot find telnet port in config file."
            )
            return

        if telnet_pass is None:
            logger.critical("7Days To Die: ERROR... cannot find telnet password.")
            return

        # Open connection with timeout
        timeout = 5
        self._telnet.open("localhost", int(telnet_port), timeout)

        # If the password is anything but a blank string.
        if telnet_pass != "":
            self._telnet.write(telnet_pass.encode("ascii") + b"\n")

        shutdown_command = "shutdown"

        self._telnet.write(shutdown_command.encode("ascii") + b"\n")

        # Give server time to shutdown
        time.sleep(10)

        # Check forthe process
        process = _get_proc_by_name(self._game_executable)

        if process is None:
            update_dict = {"game_pid": None}
            game_qry.update(update_dict)
            DATABASE.session.commit()

        else:
            logger.critical(
                "7Days To Die: Used telnet to shutdown the game but it did not do so..."
            )
