from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class SteamGameClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool) -> None:
        super(SteamGameClient, self).__init__(urls, verbose)

    def install_steam_app(
        self, steam_install_path, steam_id, install_dir, user="anonymous", password=None
    ):
        post_url = self._urls.get_install_url()

        payload = {
            "steam_install_path": steam_install_path,
            "steam_id": steam_id,
            "install_dir": install_dir,
            "user": user,
            "password": password,
        }

        if self._verbose:
            print("Installing Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url, payload=payload)
        self.handle_response(response)

    def remove_steam_app(self):
        post_url = self._urls.get_remove_url()

        if self._verbose:
            print("Removing Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def update_steam_app(self):
        post_url = self._urls.get_update_url()

        if self._verbose:
            print("Updating Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)
