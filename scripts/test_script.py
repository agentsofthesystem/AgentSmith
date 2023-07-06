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

    steam_install_path = r"C:\Program Files (x86)\Steam"
    steam_id = "1829350"
    install_path = r"C:\Users\Shadow\Desktop\STEAM\vrising"

    client.app.install_app(steam_install_path, steam_id, install_path)

    # client.app.remove_app()
    # client.app.update_app()

    # client.app.start_app()
    # client.app.stop_app()
    # client.app.restart_app()
    # client.app.get_status()

    # client.access.generate_access_key()
    # client.access.verify_access_key()


if __name__ == "__main__":
    main()
