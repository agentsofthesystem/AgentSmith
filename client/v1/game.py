from application.common.constants import FileModes
from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class SupportedGameClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool, token: str = None) -> None:
        super(SupportedGameClient, self).__init__(urls, verbose, token)

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

    def get_game_by_name(self, game_name):
        get_url = self._urls.get_game_by_name_url(game_name)

        if self._verbose:
            print(f"Getting Specific Game: {game_name}")
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

    def uninstall(self, game_name):
        post_url = self._urls.get_game_uninstall_url(game_name)

        if self._verbose:
            print(f"Uninstalling Game: {game_name}")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

        if response.status_code == 200:
            return True
        else:
            return False

    def create_argument(
        self,
        game_name: str,
        argument_name: str,
        game_arg_value: str,
        is_permanent: bool = False,
        required: bool = False,
        file_mode: FileModes = FileModes.NOT_A_FILE.value,
        use_equals: bool = False,
        use_quotes: bool = True,
    ):
        post_url = self._urls.get_arguments_url()

        payload = {
            "game_name": game_name,
            "game_arg": argument_name,
            "game_arg_value": game_arg_value,
            "is_permanent": is_permanent,
            "required": required,
            "file_mode": file_mode,
            "use_equals": use_equals,
            "use_quotes": use_quotes,
        }

        if self._verbose:
            print("Creating System Argument:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url, payload=payload)
        self.handle_response(response)

        if response.status_code == 200:
            output = response.json()
            argument_id = output["game_arg_id"]
        else:
            print("Error: Unable to create argument.")
            argument_id = -1

        return argument_id

    def get_all_arguments(self):
        get_url = self._urls.get_arguments_url()

        if self._verbose:
            print("Getting All System Arguments:")
            print(f"Get Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)

        output = response.json()

        return output

    def get_argument_by_game_name(self, game_name):
        game_output = self.get_games()
        arg_output = self.get_all_arguments()
        arg_list = []
        game_id = -1

        for game in game_output["items"]:
            if game["game_name"] == game_name:
                game_id = game["game_id"]
                break

        if game_id == -1:
            print("Error Game Does not exist!")
            return

        for arg in arg_output["items"]:
            if arg["game_id"] == game_id:
                arg_list.append(arg)

        if arg_list == []:
            print("Error: No Arguments found")
            return []

        return arg_list

    def get_argument_by_name(self, game_name, argument_name):
        get_url = self._urls.get_argument_by_name_url(game_name, argument_name)

        if self._verbose:
            print(f"Getting Game {game_name} Argument by name: {argument_name}")
            print(f"Post Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)

        output = response.json()

        if response.status_code == 200:
            output = response.json()

            items = output["items"]

            if items == []:
                items = None
            else:
                items = items[0]

        else:
            items = None

        return items

    def get_argument_by_id(self, argument_id):
        get_url = self._urls.get_argument_by_id_url(argument_id)

        if self._verbose:
            print(f"Getting System Argument by id: {argument_id}")
            print(f"Post Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)

        if response.status_code == 200:
            output = response.json()
            items = output["items"]

            if items == []:
                items = None

        else:
            items = None

        return items

    def update_argument_by_name(self, game_name, argument_name, new_value, **kwargs):
        patch_url = self._urls.get_argument_by_name_url(game_name, argument_name)

        payload = {"game_arg": argument_name, "game_arg_value": new_value}

        payload.update(kwargs)

        if self._verbose:
            print(f"Updating Game {game_name} Argument by name: {argument_name}")
            print(f"Patch Url: {patch_url}")

        response = self.make_request(RequestTypes.PATCH, patch_url, payload=payload)
        self.handle_response(response)

    def update_argument_by_id(self, argument_id, new_value, **kwargs):
        patch_url = self._urls.get_argument_by_id_url(argument_id)

        payload = {"game_arg_value": new_value}

        payload.update(kwargs)

        if self._verbose:
            print(f"Updating Argument ID: {argument_id}")
            print(f"Patch Url: {patch_url}")

        response = self.make_request(RequestTypes.PATCH, patch_url, payload=payload)
        self.handle_response(response)

        if response.status_code == 200:
            return True
        else:
            return False

    def delete_argument_by_id(self, argument_id):
        delete_url = self._urls.get_argument_by_id_url(argument_id)

        if self._verbose:
            print(f"Deleting Argument ID: {argument_id}")
            print(f"Patch Url: {delete_url}")

        response = self.make_request(RequestTypes.DELETE, delete_url)
        self.handle_response(response)

        if response.status_code == 200:
            return True
        else:
            return False
