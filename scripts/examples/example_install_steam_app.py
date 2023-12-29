import os
import platform
import sys

current_file_path = os.path.abspath(__file__)
examples_folder = os.path.dirname(current_file_path)
scripts_folder = os.path.dirname(examples_folder)
app_folder = os.path.dirname(scripts_folder)

sys.path.append(app_folder)

from operator_client import Operator


def main():
    hostname = "http://127.0.0.1"
    port = "5000"

    client = Operator(hostname, port=port, verbose=True)

    steam_id = "1829350"  # Steam id for vrising private server

    # Example to install Vrising Game Server
    if platform.system() == "Windows":
        steam_install_path = r"C:\STEAM_TEST\steam"
        install_path = r"C:\STEAM_TEST\vrising"
    else:
        steam_install_path = "/c/STEAM_TEST/steam"
        install_path = "/c/STEAM_TEST/vrising"

    client.steam.install_steam_app(steam_install_path, steam_id, install_path)


if __name__ == "__main__":
    main()
