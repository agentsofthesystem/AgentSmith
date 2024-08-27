import argparse
import os
import yaml


def set_version(new_version: str):
    version_file = os.path.join("application", "static", "version.yml")

    with open(version_file, "r") as ver_file:
        version_data = yaml.safe_load(ver_file)
        ver_file.close()

    with open(version_file, "w") as ver_file:
        version_data["version"] = new_version
        yaml.dump(version_data, ver_file)
        ver_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=str, help="New Version String")
    args = parser.parse_args()

    if args.version is None:
        print("Error: Missing Argument! Try again.")
    else:
        print(f"Version String: {args.version}")
        set_version(args.version)
