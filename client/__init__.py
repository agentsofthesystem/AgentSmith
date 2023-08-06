import sys
import validators

from client.v1.urls import AppUrls
from client.v1.access import AccessClient
from client.v1.executable import GenericExecutableClient
from client.v1.game import SupportedGameClient
from client.v1.steam import SteamGameClient


class Client:
    def __init__(self, hostname, port=None, verbose=False) -> None:
        self._host = hostname if port is None else f"{hostname}:{port}"

        if not validators.url(self._host):
            print(f"Client: Error! Unformatted Url: {self._host}")
            sys.exit(1)

        urls = AppUrls(self._host)
        self._urls = urls

        self.access = AccessClient(urls, verbose)
        self.steam = SteamGameClient(urls, verbose)
        self.exe = GenericExecutableClient(urls, verbose)
        self.game = SupportedGameClient(urls, verbose)
