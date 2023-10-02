import PyInstaller.__main__


def main():
    # This is the command line version of what this script is attempting to capture.
    """
    pyinstaller \
        --add-data="./application/gui/resources/keeper.png;./application/gui/resources" \
        --add-data="./application/source/games/resources/*;./application/source/games/resources" \
        --onefile launch.py \
        --debug all
    """

    PyInstaller.__main__.run(
        [
            "launch.py",
            "--onefile",
            "--icon=./application/gui/resources/keeper.ico",
            "--add-data=./application/gui/resources/keeper.png;./application/gui/resources",
            "--add-data=./application/source/games/*.py;./application/source/games",
            "--add-data=./application/source/games/resources/*;./application/source/games/resources",
            "--clean",
        ]
    )


if __name__ == "__main__":
    main()
