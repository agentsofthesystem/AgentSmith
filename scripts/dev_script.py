import os
import platform
import sys

current_file_path = os.path.abspath(__file__)
parent_folder = os.path.dirname(current_file_path)
app_folder = os.path.dirname(parent_folder)

sys.path.append(app_folder)

from client import Client


def main():
    print("Hello World!")

    hostname = "http://localhost"
    port = "3000"

    client = Client(hostname, port=port, verbose=True)

    # This comes directly from the game's own example batch file.
    app_name = "VRisingServer.exe"

    persistent_data_path = r"C:\Users\joshu\OneDrive\Desktop\STEAM\vrising\save-data"
    log_file_path = (
        r"C:\Users\joshu\OneDrive\Desktop\STEAM\vrising\logs\VRisingServer.log"
    )

    if platform.system() == "Windows":
        app_path = r"C:\Users\Shadow\Desktop\STEAM\vrising"
    else:
        app_path = "/c/Users/joshu/OneDrive/Desktop/STEAM/vrising"

    input_args = {
        "-persistentDataPath": f"{persistent_data_path}",
        "-serverName": "My Server",
        "-saveName": "world1",
        "-logFile": f"{log_file_path}",
    }

    # client.app.remove_app()
    # client.app.update_app()

    client.app.start_app(app_name, app_path, input_args=input_args)
    # client.app.stop_app()
    # client.app.restart_app()

    client.app.get_status(app_name)

    # client.access.generate_access_key()
    # client.access.verify_access_key()


if __name__ == "__main__":
    main()
