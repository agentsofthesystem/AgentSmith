from flask import Flask
from PyQt5.QtGui import QClipboard

from application.gui.intalled_games_menu import InstalledGameMenu
from application.gui.widgets.add_argument_widget import AddArgumentWidget
from application.source.nginx_manager import NginxManager
from operator_client import Operator


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
        self._server_port: str = "5000"
        self._steam_install_path: str = "NOT_SET"
        self._default_install_path: str = "NOT_SET"

        # Objects
        self._FLASK_APP: Flask = None
        self._client: Operator = None
        self._installed_games_menu: InstalledGameMenu = None
        self._add_arguments_widget: AddArgumentWidget = None
        self._global_clipboard: QClipboard = None
        self._nginx_manager: NginxManager = None
