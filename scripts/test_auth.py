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
    hostname = "http://127.0.0.1"
    port = "3000"

    test_token = "CHANGE_ME"  # Change to a real token

    # Have to make sure that FLASK_FORCE_AUTH in config.py is set to True for this to work locally.
    client = Client(hostname, port=port, verbose=True, token=test_token)

    # This end point is always open. No auth.
    result = client.app.get_health()
    print(result)

    result = client.app.get_health(secure_version=True)
    print(result)


if __name__ == "__main__":
    main()
