import os
import platform
import sys
import time

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

    # This comes directly from the game's own example batch file.
    exe_name = "VRisingServer.exe"

    persistent_data_path = "C:\\STEAM_TEST\\vrising\\save_data"
    log_file_path = "C:\\STEAM_TEST\\vrising\\logs\\VRisingServer.log"

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

    client.exe.launch_executable(exe_name, exe_path, input_args=input_args)

    time.sleep(5)
    client.exe.is_exe_alive(exe_name)
    time.sleep(5)
    client.exe.get_status(exe_name)
    time.sleep(5)
    client.exe.kill_executable(exe_name)

    # Not implemented
    # client.exe.restart_exe()


if __name__ == "__main__":
    main()
