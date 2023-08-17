from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class SupportedGameClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool) -> None:
        super(SupportedGameClient, self).__init__(urls, verbose)

    def get_games_schema(self):
        get_url = self._urls.get_games_schmea_url()

        if self._verbose:
            print(f"Getting all games:")
            print(f"Get Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)

        return response.json()

    def get_games(self):
        get_url = self._urls.get_all_games_url()

        if self._verbose:
            print(f"Getting all games:")
            print(f"Get Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)

        return response.json()

    def game_startup(self, game_name, input_args={}):
        post_url = self._urls.get_game_startup_url(game_name)

        payload = {}

        if len(input_args.keys()) > 0:
            arg_dict = {}
            for arg in input_args.keys():
                arg_dict[arg] = input_args[arg]

            payload.update({"input_args": arg_dict})

        if self._verbose:
            print(f"Starting Game: {game_name}")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url, payload=payload)
        self.handle_response(response)

    def game_shutdown(self, game_name):
        post_url = self._urls.get_game_shutdown_url(game_name)

        if self._verbose:
            print(f"Shutting down Game: {game_name}")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)
