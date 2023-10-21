import requests
import sys

from application.common import logger
from client.v1.urls import AppUrls
from enum import Enum


class RequestTypes(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseClient:
    def __init__(self, urls: AppUrls, verbose: bool, token: str = None) -> None:
        self._urls = urls
        self._verbose = verbose
        self._token = token

    def handle_response(self, response: requests.Response) -> None:
        if response.status_code == 200:
            print("Request made successfully!")
            if hasattr(response, "json") and self._verbose:
                print("Application Returned Json:")
                print(response.text)
        elif response.status_code == 401:
            print("Authorization Error: Request Made, but missing bearer token.")
        elif response.status_code == 403:
            print("Authorization Error: Token is not authorized.")
        elif response.status_code == 500:
            print("Error: 500 - Internal Server Error - It's not the client.")
            if self._verbose:
                print(response.content)
        else:
            print(f"Error: Other Response Code: {response.status_code}")
            if self._verbose:
                print(f"    {response.content}")

    def make_request(
        self,
        request_type: RequestTypes,
        request_url: str,
        parameter_list: list = [],
        payload: dict = {},
    ) -> requests.Response:
        if len(parameter_list) > 0:
            for i in range(0, len(parameter_list)):
                if i == 0:
                    request_url += f"?{parameter_list[i]}"
                else:
                    request_url += f"&{parameter_list[i]}"

        if self._verbose:
            logger.info(f"Request URL: {request_url}")

        headers = {}  # Empty by default

        if self._token:
            headers = {
                "Authorization": "Bearer " + self._token,
                "Content-Type": "application/json",
            }

        if request_type == RequestTypes.GET:
            response = requests.get(request_url, headers=headers)
        elif request_type == RequestTypes.POST:
            response = requests.post(request_url, json=payload, headers=headers)
        elif request_type == RequestTypes.PATCH:
            response = requests.patch(request_url, json=payload, headers=headers)
        elif request_type == RequestTypes.DELETE:
            response = requests.delete(request_url, headers=headers)
        else:
            print(
                "BaseClient: make_request: Error! - Unsupported request type! Exiting..."
            )
            sys.exit(1)

        return response
