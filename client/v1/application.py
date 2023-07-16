from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class ApplicationClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool) -> None:
        super(ApplicationClient, self).__init__(urls, verbose)

    def install_app(
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

    def remove_app(self):
        post_url = self._urls.get_remove_url()

        if self._verbose:
            print("Removing Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def update_app(self):
        post_url = self._urls.get_update_url()

        if self._verbose:
            print("Updating Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def start_app(self, app_name, app_path, input_args={}):
        post_url = self._urls.get_start_url()

        payload = {
            "app_name": app_name,
            "app_path": app_path,
        }

        if len(input_args.keys()) > 0:
            arg_dict = {}
            for arg in input_args.keys():
                arg_dict[arg] = input_args[arg]

            payload.update({"input_args": arg_dict})

        if self._verbose:
            print("Starting Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url, payload=payload)
        self.handle_response(response)

    def stop_app(self, app_name):
        post_url = self._urls.get_stop_url()

        payload = {
            "app_name": app_name,
        }

        if self._verbose:
            print("Stopping Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url, payload=payload)
        self.handle_response(response)

    def restart_app(self):
        post_url = self._urls.get_restart_url()

        if self._verbose:
            print("Restarting Application:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def get_status(self, app_name: str):
        get_url = self._urls.get_status_url()

        if self._verbose:
            print("Obtaining Application Status:")
            print(f"Get Url: {get_url}")

        response = self.make_request(
            RequestTypes.GET, get_url, parameter_list=[f"app_name={app_name}"]
        )
        self.handle_response(response)

    def is_app_alive(self, app_name: str):
        get_url = self._urls.get_alive_url()

        if self._verbose:
            print("Obtaining Application Alive Status:")
            print(f"Get Url: {get_url}")

        response = self.make_request(
            RequestTypes.GET, get_url, parameter_list=[f"app_name={app_name}"]
        )
        self.handle_response(response)
