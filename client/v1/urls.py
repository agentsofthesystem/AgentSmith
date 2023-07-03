class AppUrls:
    BASE_URL = "{host_name}/{api_version}"

    def __init__(self, host: str) -> None:
        self._host = host
        self._api_version = "v1"

    @property
    def base_url(self) -> str:
        return self.BASE_URL.format(host_name=self._host, api_version=self._api_version)

    def get_start_url(self) -> str:
        return f"{self.base_url}/app/start"

    def get_stop_url(self) -> str:
        return f"{self.base_url}/app/stop"

    def get_restart_url(self) -> str:
        return f"{self.base_url}/app/restart"

    def get_status_url(self) -> str:
        return f"{self.base_url}/app/status"

    def get_key_generation_url(self) -> str:
        return f"{self.base_url}/key/generate"

    def get_key_verification_url(self) -> str:
        return f"{self.base_url}/key/verify"
