# -*- coding: utf-8 -*-
from flask import Flask

from application.gui.intalled_games_menu import InstalledGameMenu
from application.gui.widgets.game_control_widget import GameControlWidget
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
        self._game_control_widget: GameControlWidget = None
