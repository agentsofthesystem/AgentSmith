import PyInstaller.__main__

from sys import platform


def main():
    # On windows, the separator is a semi-colon. On linux it's a colon.
    if platform == "win32":
        sep = ";"
    else:
        sep = ":"

    PyInstaller.__main__.run(
        [
            "agent-smith.py",
            "--onefile",
            "--icon=./application/gui/resources/agent-black.ico",
            f"--add-data=./application/config/nginx/*{sep}./application/config/nginx",  # noqa: E501
            f"--add-data=./application/gui/resources/agent-white.png{sep}u./application/gui/resources",  # noqa: E501
            f"--add-data=./application/gui/resources/agent-green.png{sep}./application/gui/resources",  # noqa: E501
            f"--add-data=./application/games/*.py{sep}./application/games",
            f"--add-data=./application/games/resources/*{sep}./application/games/resources",  # noqa: E501
            f"--add-data=./application/alembic/alembic.ini{sep}./application/alembic",
            f"--add-data=./application/alembic/env.py{sep}./application/alembic",
            f"--add-data=./application/alembic/script.py.mako{sep}./application/alembic",  # noqa: E501
            f"--add-data=./application/alembic/versions/*.py{sep}./application/alembic/versions",  # noqa: E501
            "--hidden-import=xml.etree.ElementTree",
            "--hidden-import=telnetlib",
            "--clean",
        ]
    )


if __name__ == "__main__":
    main()
