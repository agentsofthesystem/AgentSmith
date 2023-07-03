from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class ApplicationClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool) -> None:
        super(ApplicationClient, self).__init__(urls, verbose)

    def start_app(self):
        post_url = self._urls.get_start_url()

        if self._verbose:
            print("Starting Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def stop_app(self):
        post_url = self._urls.get_stop_url()

        if self._verbose:
            print("Stopping Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def restart_app(self):
        post_url = self._urls.get_restart_url()

        if self._verbose:
            print("Restarting Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def get_status(self):
        get_url = self._urls.get_status_url()

        if self._verbose:
            print("Obtaining Application Status:")
            print(f"Get Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)
