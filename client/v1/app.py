from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class BaseAppClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool, token: str = None) -> None:
        super(BaseAppClient, self).__init__(urls, verbose, token)

    def get_health(self, secure_version=False):
        if secure_version:
            get_url = self._urls.get_secure_health_url()
        else:
            get_url = self._urls.get_health_url()

        if self._verbose:
            print("Getting Health:")
            print(f"Get Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)

        if response.status_code == 200:
            output = response.json()
        else:
            output = None

        return output

    def create_setting(self, setting_name: str, setting_value: str):
        post_url = self._urls.get_settings_url()

        payload = {"setting_name": setting_name, "setting_value": setting_value}

        if self._verbose:
            print("Creating System Setting:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url, payload=payload)
        self.handle_response(response)

        if response.status_code == 200:
            output = response.json()
            setting_id = output["setting_id"]
        else:
            print("Error: Unable to create setting.")
            setting_id = 1

        return setting_id

    def get_all_settings(self):
        get_url = self._urls.get_settings_url()

        if self._verbose:
            print("Getting All System Settings:")
            print(f"Get Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)

        output = response.json()

        return output

    def get_setting_by_name(self, setting_name):
        get_url = self._urls.get_settings_by_name_url(setting_name)

        if self._verbose:
            print(f"Getting System Setting by name: {setting_name}")
            print(f"Post Url: {get_url}")

        response = self.make_request(RequestTypes.GET, get_url)
        self.handle_response(response)

        output = response.json()

        if response.status_code == 200:
            output = response.json()
            items = output["items"][0]["setting_value"]

            if items == []:
                items = None

        else:
            items = None

        return items

    def get_settings_by_id(self, setting_id):
        get_url = self._urls.get_settings_by_id_url(setting_id)

        if self._verbose:
            print(f"Getting System Setting by id: {setting_id}")
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

    def update_setting_by_name(self, setting_name, new_value):
        patch_url = self._urls.get_settings_by_name_url(setting_name)

        payload = {"setting_name": setting_name, "setting_value": new_value}

        if self._verbose:
            print(f"Updating System Setting by name: {setting_name}")
            print(f"Patch Url: {patch_url}")

        response = self.make_request(RequestTypes.PATCH, patch_url, payload=payload)
        self.handle_response(response)
