import os
import platform
import sys
import time

current_file_path = os.path.abspath(__file__)
parent_folder = os.path.dirname(current_file_path)
app_folder = os.path.dirname(parent_folder)

sys.path.append(app_folder)

from client import Client


def main():
    hostname = "http://localhost"
    port = "3000"

    client = Client(hostname, port=port, verbose=True)

    # This comes directly from the game's own example batch file.
    exe_name = "VRisingServer.exe"

    persistent_data_path = (
        "C:\\STEAM_TEST\\vrising\\save_data"
    )
    log_file_path = (
        "C:\\STEAM_TEST\\vrising\\logs\\VRisingServer.log"
    )

    if platform.system() == "Windows":
        exe_path = r"C:\STEAM_TEST\vrising"
    else:
        exe_path = "/c/STEAM_TEST/vrising"

    input_args = {
        "-persistentDataPath": f"{persistent_data_path}",
        "-serverName": "My Server",
        "-saveName": "world1",
        "-logFile": f"{log_file_path}",
    }

    # client.steam.remove_steam_app()
    # client.steam.update_steam_app()

    client.exe.launch_executable(exe_name, exe_path, input_args=input_args)
    # client.exe.kill_executable(exe_name)
    # client.exe.restart_exe()

    # time.sleep(2)

    # client.exe.is_exe_alive(exe_name)
    # client.exe.get_status(exe_name)

    # client.access.generate_access_key()
    # client.access.verify_access_key()


if __name__ == "__main__":
    main()
