import os
import platform
import sys
import time

current_file_path = os.path.abspath(__file__)
parent_folder = os.path.dirname(current_file_path)
app_folder = os.path.dirname(parent_folder)

sys.path.append(app_folder)

from operator_client import Operator


def main():
    hostname = "http://127.0.0.1"
    port = "3000"

    client = Operator(hostname, port=port, verbose=True)

    game_name = "vrising"

    persistent_data_path = r"C:\STEAM_TEST\installs\vrising\save_data"
    log_file_path = r"C:\STEAM_TEST\installs\vrising\logs\VRisingServer.log"

    # if platform.system() == "Windows":
    #     exe_path = r"C:\STEAM_TEST\vrising"
    # else:
    #     exe_path = "/c/STEAM_TEST/vrising"

    input_args = {
        "-persistentDataPath": f"{persistent_data_path}",
        "-serverName": "My Server",
        "-saveName": "world1",
        "-logFile": f"{log_file_path}",
    }

    # client.game.game_startup(game_name, input_args=input_args)

    # time.sleep(30)

    # client.game.game_shutdown(game_name)
    schema = client.game.get_games_schema()
    print(schema)


if __name__ == "__main__":
    main()
