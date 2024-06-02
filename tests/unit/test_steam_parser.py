import os

from application.common.steam_manifest_parser import read_acf, parser, read_dir


class TestSteamManifestParser:
    ACF_FILE_NAME = "appmanifest_1829350.acf"
    ACF_FILE_PATH = ""
    ACF_FOLDER = ""

    @classmethod
    def setup_class(cls):
        # Get the current working directory
        current_location = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_location)
        cls.ACF_FOLDER = os.path.join(current_folder, "resources", "steam_manifest")
        cls.ACF_FILE_PATH = os.path.join(
            current_folder, "resources", "steam_manifest", cls.ACF_FILE_NAME
        )

    @classmethod
    def teardown_class(cls):
        pass

    def test_read_dir(self):
        steamapps = read_dir(self.ACF_FOLDER)
        assert len(steamapps) == 1
        assert "1829350" in steamapps

    def test_read_acf(self):
        acf = read_acf(self.ACF_FILE_PATH)
        assert acf["appid"] == "1829350"
        assert acf["name"] == "V Rising Dedicated Server"
        assert acf["StateFlags"] == "4"
        assert acf["installdir"] == "VRisingDedicatedServer"
