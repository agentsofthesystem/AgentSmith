import os
import platform
import sys

current_file_path = os.path.abspath(__file__)
examples_folder = os.path.dirname(current_file_path)
scripts_folder = os.path.dirname(examples_folder)
app_folder = os.path.dirname(scripts_folder)

sys.path.append(app_folder)

from application.common.constants import FileModes
from operator_client import Operator


def main():
    hostname = "http://127.0.0.1"
    port = "5000"

    client = Operator(hostname, port=port, verbose=True)

    arg_1_value = client.game.get_argument_by_name("vrising", "-test123")

    if arg_1_value is None:
        arg_id_1 = client.game.create_argument(
            "vrising", "-test123", "foobar", True, True, True
        )
        print(f"New Argument is id: {arg_id_1}")
    else:
        arg_id_1 = arg_1_value["game_arg_id"]
        print(f"Existing Argument is id: {arg_id_1}")

    client.game.update_argument_by_name(
        "vrising", "-test123", "abc123", file_mode=FileModes.DIRECTORY.value
    )

    arg_1_value_again = client.game.get_argument_by_name("vrising", "-test123")
    print(arg_1_value_again)

    by_id = client.game.get_argument_by_id(arg_id_1)
    print("****************************")
    print(by_id)
    print("****************************")

    all_args = client.game.get_all_arguments()

    print("****************************")
    print(all_args)
    print("****************************")

    # client.game.update_argument_by_name(
    #     "vrising", "-persistentDataPath", "C:/STEAM_TEST/installs/vrising/save_data", is_permanent=True
    # )
    # client.game.update_argument_by_name(
    #     "vrising", "-serverName", "world", is_permanent=True
    # )
    # client.game.update_argument_by_name(
    #     "vrising", "-saveName", "world1", is_permanent=True
    # )
    # client.game.update_argument_by_name(
    #     "vrising", "-logFile", "C:/STEAM_TEST/installs/vrising/logs/VRisingServer.log", is_permanent=True
    # )
    # client.game.update_argument_by_name(
    #     "vrising", "-serverPort", "27015", is_permanent=True
    # )


if __name__ == "__main__":
    main()
