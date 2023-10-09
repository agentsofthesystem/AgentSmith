from flask import Flask

from application.gui.intalled_games_menu import InstalledGameMenu
from application.gui.widgets.add_argument_widget import AddArgumentWidget
from application.gui.widgets.game_manager_widget import GameManagerWidget
from client import Client


class GuiGlobals:
    def __init__(self):
        # For ArgParse
        self._DESCRIPTION_MSG = """ """
        self._EPILOG_MSG = """
            Examples:
        """

        # Primitive types
        self._VERSION: str = "_alpha"
        self._server_host: str = "127.0.0.1"
        self._server_port: str = "3000"
        self._steam_install_path: str = "NOT_SET"

        # Objects
        self._FLASK_APP: Flask = None
        self._client: Client = None
        self._installed_games_menu: InstalledGameMenu = None
        self._add_arguments_widget: AddArgumentWidget = None
