from client.common.base_client import BaseClient, RequestTypes
from client.v1.urls import AppUrls


class AccessClient(BaseClient):
    def __init__(self, urls: AppUrls, verbose: bool) -> None:
        super(AccessClient, self).__init__(urls, verbose)

    def generate_access_key(self):
        post_url = self._urls.get_key_generation_url()

        if self._verbose:
            print("Generating Application Key:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)

    def verify_access_key(self):
        post_url = self._urls.get_key_verification_url()

        if self._verbose:
            print("Verifying Application Key:")
            print(f"Post Url: {post_url}")

        response = self.make_request(RequestTypes.POST, post_url)
        self.handle_response(response)
