
from client.access_keys import AccessKeysClient

class PGSMAgentClient():

    def __init__(self) -> None:

        self._key_client = AccessKeysClient()


    def start_application(self, file_name, file_path, args) -> bool:

        return True     