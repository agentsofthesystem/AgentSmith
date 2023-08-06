class AppUrls:
    BASE_URL = "{host_name}/{api_version}"

    def __init__(self, host: str) -> None:
        self._host = host
        self._api_version = "v1"

    @property
    def base_url(self) -> str:
        return self.BASE_URL.format(host_name=self._host, api_version=self._api_version)

    ###############################################################################
    ###############################################################################
    ## Steam App Urls
    ###############################################################################
    ###############################################################################

    def get_install_url(self) -> str:
        return f"{self.base_url}/steam/app/install"

    def get_remove_url(self) -> str:
        return f"{self.base_url}/steam/app/remove"

    def get_update_url(self) -> str:
        return f"{self.base_url}/steam/app/update"

    ###############################################################################
    ###############################################################################
    ### Generic Executable Urls
    ###############################################################################
    ###############################################################################

    def get_exe_launch_url(self) -> str:
        return f"{self.base_url}/exe/launch"

    def get_exe_kill_url(self) -> str:
        return f"{self.base_url}/exe/kill"

    def get_exe_restart_url(self) -> str:
        return f"{self.base_url}/exe/restart"

    def get_exe_status_url(self) -> str:
        return f"{self.base_url}/exe/status"

    def get_exe_alive_url(self) -> str:
        return f"{self.base_url}/exe/alive"

    ###############################################################################
    ###############################################################################
    ## Supported Game Related Urls
    ###############################################################################
    ###############################################################################

    def get_game_startup_url(self, game_name) -> str:
        return f"{self.base_url}/game/startup/{game_name}"

    ###############################################################################
    ###############################################################################
    ## Key/Access Related Urls
    ###############################################################################
    ###############################################################################

    def get_key_generation_url(self) -> str:
        return f"{self.base_url}/key/generate"

    def get_key_verification_url(self) -> str:
        return f"{self.base_url}/key/verify"
