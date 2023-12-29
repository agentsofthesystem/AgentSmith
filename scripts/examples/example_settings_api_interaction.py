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

    setting_id_1 = None
    setting_id_2 = None

    client = Operator(hostname, port=port, verbose=True)

    setting_1_value = client.app.get_setting_by_name("test_setting_1")

    if setting_1_value is None:
        setting_id_1 = client.app.create_setting("test_setting_1", "abc")
    else:
        setting_id_1 = setting_1_value["setting_id"]

    setting_2_value = client.app.get_setting_by_name("test_setting_2")

    if setting_2_value is None:
        setting_id_2 = client.app.create_setting("test_setting_2", "abc")
    else:
        setting_id_3 = setting_2_value["setting_id"]

    client.app.update_setting_by_name("test_setting_2", "123")

    all_settings = client.app.get_all_settings()

    print(f"Setting 1 ID: {setting_id_1}")
    print(f"Setting 2 ID: {setting_id_2}")
    print(all_settings)


if __name__ == "__main__":
    main()
