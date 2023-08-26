# -*- coding: utf-8 -*-


class GuiGlobals:
    def __init__(self):
        self._DESCRIPTION_MSG = """ """

        self._EPILOG_MSG = """
            Examples:
        """

        self._VERSION = "_alpha"
        self._FLASK_APP = None

        self._server_host = "127.0.0.1"
        self._server_port = "3000"
        self._client = None
        self._installed_games_menu = None

        self._steam_install_path = "NOT_SET"
