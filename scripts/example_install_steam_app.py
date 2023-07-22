import os
import platform
import sys

current_file_path = os.path.abspath(__file__)
parent_folder = os.path.dirname(current_file_path)
app_folder = os.path.dirname(parent_folder)

sys.path.append(app_folder)

from client import Client


def main():
    hostname = "http://localhost"
    port = "3000"

    client = Client(hostname, port=port, verbose=True)

    steam_id = "1829350"  # Steam id for vrising private server

    # Example to install Vrising Game Server
    if platform.system() == "Windows":
        steam_install_path = r"C:\STEAM\steam"
        install_path = r"C:\STEAM\vrising"
    else:
        steam_install_path = "/c/STEAM_TEST/steam"
        install_path = "/c/STEAM_TEST/vrising"

    client.steam.install_steam_app(steam_install_path, steam_id, install_path)


if __name__ == "__main__":
    main()
