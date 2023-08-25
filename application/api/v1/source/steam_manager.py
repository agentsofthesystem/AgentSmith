from application.common import toolbox


import os
import subprocess

from datetime import datetime
from pysteamcmd.steamcmd import Steamcmd
from sqlalchemy import exc

from application.api.v1.source.models.games import Games
from application.api.v1.source.models.game_arguments import GamesArguments
from application.common import logger
from application.common.exceptions import InvalidUsage
from application.extensions import DATABASE


class SteamManager:
    def __init__(self, steam_install_dir) -> None:
        if not os.path.exists(steam_install_dir):
            os.makedirs(steam_install_dir, mode=0o777, exist_ok=True)

        toolbox.recursive_chmod(steam_install_dir)

        self._steam = Steamcmd(steam_install_dir)

        self._steam.install(force=True)

        toolbox.recursive_chmod(steam_install_dir)

        self._steamcmd_exe = self._steam.steamcmd_exe
        self._steam_install_dir = steam_install_dir

    def save_game_arguments(self, steam_id: str, input_args: {}):
        game_obj = Games.query.filter_by(game_steam_id=steam_id).first()
        game_id = game_obj.game_id

        for key, value in input_args.items():
            arg_qry = GamesArguments.query.filter_by(game_arg=key, game_id=game_id)

            if arg_qry.first() is None:
                new_arg = GamesArguments()
                new_arg.game_arg = key
                new_arg.game_arg_value = value
                new_arg.game_id = game_id
                DATABASE.session.add(new_arg)

            else:
                arg_qry.update({key: value})

            DATABASE.session.commit()

    def install_steam_app(
        self, steam_id, installation_dir, user="anonymous", password=None
    ):
        if not os.path.exists(installation_dir):
            os.makedirs(installation_dir, mode=0o777, exist_ok=True)

        # If exists in DB this is the record
        game_qry = Games.query.filter_by(game_steam_id=steam_id)

        # If the object exists, then the user has already attempted installation once. Do not make a new
        # databse record again.
        if not game_qry.first():
            new_game = Games()
            new_game.game_steam_id = int(steam_id)
            new_game.game_install_dir = installation_dir
            DATABASE.session.add(new_game)
        else:
            # If it exists, just update the timestamp so the user knows the last time this game was installed/updated.
            time_now = datetime.now()
            update_dict = {"game_last_update": time_now}
            game_qry.update(update_dict)

        try:
            DATABASE.session.commit()
        except exc.SQLAlchemyError:
            message = (
                "SteamManager: install_steam_app -> Error: Failed to update database."
            )
            logger.critical(message)
            raise InvalidUsage(message, status_code=500)

        return self._install_gamefiles(
            gameid=steam_id,
            game_install_dir=installation_dir,
            user=user,
            password=password,
            validate=True,
        )

    def _install_gamefiles(
        self, gameid, game_install_dir, user="anonymous", password=None, validate=False
    ):
        """
        Installs gamefiles for dedicated server. This can also be used to update the gameserver.
        :param gameid: steam game id for the files downloaded
        :param game_install_dir: installation directory for gameserver files
        :param user: steam username (defaults anonymous)
        :param password: steam password (defaults None)
        :param validate: should steamcmd validate the gameserver files (takes a while)
        :return: subprocess call to steamcmd
        """
        if validate:
            validate = "validate"
        else:
            validate = None

        steamcmd_params = (
            self._steamcmd_exe,
            "+login {} {}".format(user, password),
            "+force_install_dir {}".format(game_install_dir),
            "+app_update {}".format(gameid),
            "{}".format(validate),
            "+quit",
        )

        # Need to add steamservice.so to the system path
        if self._steam.platform == "Linux":
            library_path = os.path.join(self._steam_install_dir, "linux64")
            update_environ = os.environ
            update_environ["LD_LIBRARY_PATH"] = library_path
            return subprocess.Popen(steamcmd_params, env=update_environ)
        else:
            # Otherwise, on windows, it's expected that steam is installed.
            return subprocess.Popen(steamcmd_params)
