from pysteamcmd.steamcmd import Steamcmd

class SteamManager():
    
    def __init__(self, steam_install_dir) -> None:

        self._steam = Steamcmd(steam_install_dir)

        self._steam.install()

    def install_steam_app(self, steam_id, installation_dir, user='anonymous', password=None):

        self._steam.install_gamefiles(gameid=steam_id, 
                                      game_install_dir=installation_dir, 
                                      user=user, 
                                      password=password, 
                                      validate=True)
        
    
