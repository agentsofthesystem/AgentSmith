import PyInstaller.__main__

from sys import platform


def main():
    # On windows, the separator is a semi-colon. On linux it's a colon.
    if platform == "win32":
        sep = ';'
    else:
        sep = ':'

    PyInstaller.__main__.run(
        [
            "launch.py",
            "--onefile",
            "--icon=./application/gui/resources/keeper.ico",
            f"--add-data=./application/gui/resources/keeper.png{sep}./application/gui/resources",
            f"--add-data=./application/source/games/*.py{sep}./application/source/games",
            f"--add-data=./application/source/games/resources/*{sep}./application/source/games/resources",
            "--clean",
        ]
    )


if __name__ == "__main__":
    main()
