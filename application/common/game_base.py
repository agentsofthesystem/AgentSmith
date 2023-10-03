import abc
import time

from application.common import logger
from application.common.game_argument import GameArgument
from application.common.exceptions import InvalidUsage
from application.source.models.games import Games
from application.source.models.game_arguments import GameArguments


class BaseGame:
    DEFAULT_WAIT_PERIOD = 5

    def __init__(self) -> None:
        self._game_args: dict = {}
        self._game_name: str = None
        self._game_pretty_name: str = None
        self._game_executable: str = None
        self._game_steam_id: str = None
        self._game_installed: bool = False
        self._game_info_url: str = ""

    @abc.abstractmethod
    def startup(self) -> None:
        """Implementation Specific Startup Routine."""
        self._input_check_routine()

    @abc.abstractmethod
    def shutdown(self) -> None:
        """Implementation Specific shutdown Routine."""
        self._input_check_routine()

    def restart(self, wait_period=DEFAULT_WAIT_PERIOD) -> None:
        """Simple Routine to shutdown and re-run the startup routines."""
        self.shutdown()

        time.sleep(wait_period)

        self.startup()

    def _is_game_installed(self) -> bool:
        if not self._game_steam_id:
            logger.warning(
                "BaseGame: _is_game_installed - Need _game_steam_id to check if game is installed."
            )
            return False

        game_qry = Games.query.filter_by(game_steam_id=self._game_steam_id)

        if not game_qry.first():
            logger.debug(
                f"BaseGame: _is_game_installed - Game with SteamID {self._game_steam_id} not installed."
            )
            return False

        return True

    def _input_check_routine(self) -> None:
        if self._check_all_inputs():
            if self._game_executable and self._game_name and self._game_steam_id:
                message = f"BaseGame: {self._game_executable} is missing an argument."
                logger.error(message)
                raise InvalidUsage(message, status_code=400)
            elif self._game_executable is None:
                message = f"BaseGame: User must supply an executable name to attr: _game_executable."
                logger.error(message)
                raise InvalidUsage(message, status_code=400)
            elif self._game_name is None:
                message = f"BaseGame: User must supply a game name to attr: _game_name."
                logger.error(message)
                raise InvalidUsage(message, status_code=400)
            elif self._game_steam_id is None:
                message = (
                    f"BaseGame: User must supply a valid steam id attr: _game_steam_id."
                )
                logger.error(message)
                raise InvalidUsage(message, status_code=400)
            elif not self._game_installed:
                message = f"BaseGame: User must have previously installed the game."
                logger.error(message)
                raise InvalidUsage(message, status_code=400)

    def _get_argument_list(self) -> []:
        return list(self._game_args.keys())

    def _get_argument_dict(self) -> []:
        return self._game_args

    def _get_command_str(self) -> str:
        arg_string = ""
        for _, arg in self._game_args.items():
            arg_string += str(arg) + " "

        return f"{self._game_executable} {arg_string}"

    def _rebuild_arguments_dict(self) -> None:
        game_qry = Games.query.filter_by(game_name=self._game_name)
        game_obj = game_qry.first()

        game_arg_objs = GameArguments.query.filter_by(game_id=game_obj.game_id).all()

        self._reset_arguments()

        for argument in game_arg_objs:
            game_arg: GameArgument = GameArgument(
                argument.game_arg,
                value=argument.game_arg_value,
                required=argument.required,
                use_equals=argument.use_equals,
                use_quotes=argument.use_quotes,
                is_permanent=argument.is_permanent,
                file_mode=argument.file_mode,
            )
            self._add_argument(game_arg)

    def _reset_arguments(self) -> None:
        self._game_args.clear()

    def _update_argument(self, arg_name, value) -> None:
        if arg_name not in self._game_args.keys():
            logger.error("BaseGame: Argument does not exist!")

        game_arg = self._game_args[arg_name]
        game_arg._value = value

    def _add_argument(self, arg: GameArgument) -> None:
        if arg._arg not in self._game_args:
            self._game_args[arg._arg] = arg
        else:
            logger.warning(f"BaseGame: Argument: {arg._arg} - Already Exists! Skipping")

    def _check_all_inputs(self) -> bool:
        args_error = not self._check_args()
        game_name_error = True if self._game_name is None else False
        game_exe_error = True if self._game_executable is None else False
        steam_id_error = True if self._game_steam_id is None else False

        return (
            args_error
            and game_name_error
            and game_exe_error
            and steam_id_error
            and not self._game_installed
        )

    def _check_args(self) -> bool:
        is_arg_missing = False

        for arg_name, arg in self._game_args.items():
            if arg._value is None and arg.is_required():
                is_arg_missing = True
                break

        return is_arg_missing
