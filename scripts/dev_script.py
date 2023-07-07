import os
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
    app_path = r"C:\Users\Shadow\Desktop\STEAM\vrising"
    input_args = (
        f'-persistentDataPath "{app_path}\save-data"'
        ' -serverName "My V Rising Server" '
        ' -saveName "world1" '
        f' -logFile "{app_path}\logs\VRisingServer.log"'
    )

    input_args = {
        "-persistentDataPath": f"{app_path}\save-data",
        "-serverName": "My Server",
        "-saveName": "world1",
        "-logFile": f"{app_path}\logs\VRisingServer.log",
    }
    # client.app.remove_app()
    # client.app.update_app()

    # client.app.start_app(app_name, app_path, input_args=input_args)
    # client.app.stop_app()
    # client.app.restart_app()

    client.app.get_status(app_name)

    # client.access.generate_access_key()
    # client.access.verify_access_key()


if __name__ == "__main__":
    main()
