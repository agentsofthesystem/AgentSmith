from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class AccessClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool, token: str = None) -> None:
        super(AccessClient, self).__init__(urls, verbose, token)

    def get_all_active_tokens(self):
        request_url = self._urls.get_active_tokens()

        if self._verbose:
            print("Generating Application token:")
            print(f"Request Url: {request_url}")

        response = self.make_request(RequestTypes.GET, request_url)
        self.handle_response(response)

        if response.status_code != 200:
            return []
        else:
            data = response.json()
            return data["items"]

    def generate_access_token(self, token_name):
        request_url = self._urls.get_token_generation_url(token_name)

        if self._verbose:
            print("Generating Application token:")
            print(f"Request Url: {request_url}")

        response = self.make_request(RequestTypes.GET, request_url)
        self.handle_response(response)

        if response.status_code == 200:
            return response.content.decode("utf-8")
        else:
            return False

    def verify_access_token(self, token_name):
        post_url = self._urls.get_token_verification_url(token_name)

        if self._verbose:
            print("Verifying Application token:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def invalidate_token(self, token_name):
        post_url = self._urls.get_token_invalidation_url(token_name)

        if self._verbose:
            print("Verifying Application token:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)
