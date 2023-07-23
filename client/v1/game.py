from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class SupportedGameClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool) -> None:
        super(SupportedGameClient, self).__init__(urls, verbose)
