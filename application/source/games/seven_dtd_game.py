from application.common import logger
from application.common.game_argument import GameArgument
from application.common.game_base import BaseGame


# NOTE - This Game is not yet implemented.


class SevenDaysToDieGame(BaseGame):
    def __init__(self) -> None:
        super(SevenDaysToDieGame, self).__init__()

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

        logger.info("Not Implemented")

    def shutdown(self) -> None:
        logger.info("Not Implemented")
