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
            "launch.py",
            "--onefile",
            "--icon=./application/gui/resources/keeper.ico",
            f"--add-data=./application/gui/resources/keeper.png{sep}./application/gui/resources",
            f"--add-data=./application/source/games/*.py{sep}./application/source/games",
            f"--add-data=./application/source/games/resources/*{sep}./application/source/games/resources",
            f"--add-data=./application/source/alembic/alembic.ini{sep}./application/source/alembic",
            f"--add-data=./application/source/alembic/env.py{sep}./application/source/alembic",
            f"--add-data=./application/source/alembic/script.py.mako{sep}./application/source/alembic",
            f"--add-data=./application/source/alembic/versions/*.py{sep}./application/source/alembic/versions",
            "--hidden-import=xml.etree.ElementTree",
            "--hidden-import=telnetlib",
            "--clean",
        ]
    )


if __name__ == "__main__":
    main()
