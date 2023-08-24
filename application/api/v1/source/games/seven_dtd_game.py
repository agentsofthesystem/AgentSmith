from application.api.v1.source.games.common.game_argument import GameArgument
from application.api.v1.source.games.common.game_base import BaseGame


# NOTE - This Game is not yet implemented.


class VrisingGame(BaseGame):
    def __init__(self) -> None:
        super(VrisingGame, self).__init__()

        self._game_name = "7dtd"
        self._game_pretty_name = "7 Days To Die"
        self._game_executable = "SevenDaysToDie.exe"
        self._game_steam_id = "294420"

        # Add Args here, can update later.
        self._add_argument(GameArgument("-arg1", value=None, required=True))
        self._add_argument(
            GameArgument("-arg2", value=None, required=True, use_quotes=True)
        )
        self._add_argument(
            GameArgument("-arg3", value=None, required=True, use_quotes=True)
        )
        self._add_argument(
            GameArgument("-arg4", value=None, required=True, use_quotes=True)
        )

    def startup(self) -> None:
        # Run base class checks
        super().startup()

        print("Not Implemented")

    def shutdown(self) -> None:
        print("Not Implemented")
