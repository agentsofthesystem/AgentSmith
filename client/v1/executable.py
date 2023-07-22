from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class GenericExecutableClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool) -> None:
        super(GenericExecutableClient, self).__init__(urls, verbose)

    def launch_executable(self, exe_name, exe_path, input_args={}):
        post_url = self._urls.get_exe_launch_url()

        payload = {
            "exe_name": exe_name,
            "exe_path": exe_path,
        }

        if len(input_args.keys()) > 0:
            arg_dict = {}
            for arg in input_args.keys():
                arg_dict[arg] = input_args[arg]

            payload.update({"input_args": arg_dict})

        if self._verbose:
            print("Starting Executable:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url, payload=payload)
        self.handle_response(response)

    def kill_executable(self, exe_name):
        post_url = self._urls.get_exe_kill_url()

        payload = {
            "exe_name": exe_name,
        }

        if self._verbose:
            print("Stopping Executable:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url, payload=payload)
        self.handle_response(response)

    def restart_exe(self):
        post_url = self._urls.get_exe_restart_url()

        if self._verbose:
            print("Restarting Executable:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def get_status(self, exe_name: str):
        get_url = self._urls.get_exe_status_url()

        if self._verbose:
            print("Obtaining Executable Status:")
            print(f"Get Url: {get_url}")

        response = self.make_request(
            RequestTypes.GET, get_url, parameter_list=[f"exe_name={exe_name}"]
        )
        self.handle_response(response)

    def is_exe_alive(self, exe_name: str):
        get_url = self._urls.get_exe_alive_url()

        if self._verbose:
            print("Obtaining Executable Alive Status:")
            print(f"Get Url: {get_url}")

        response = self.make_request(
            RequestTypes.GET, get_url, parameter_list=[f"exe_name={exe_name}"]
        )
        self.handle_response(response)
