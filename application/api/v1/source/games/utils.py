import os


@staticmethod
def get_resources_dir() -> str:
    current_file = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_file)
    resources_folder = os.path.join(current_folder, "resources")
    return resources_folder
