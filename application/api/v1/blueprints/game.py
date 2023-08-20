from enum import Enum
from flask import Blueprint, request, jsonify

from application.common import logger
from application.common.exceptions import InvalidUsage
from application.api.v1.source.games.common import utils
from application.api.v1.source.games.vrising_game import VrisingGame

game = Blueprint("game", __name__, url_prefix="/v1")

###############################################################################
###############################################################################
## Supported Game Related Endpoints
###############################################################################
###############################################################################


class SupportedGameTypes(Enum):
    VRISING = "VRISING"


@staticmethod
def _is_supported_game(game_name):
    return game_name in SupportedGameTypes._value2member_map_


@game.route("/games", methods=["GET"])
def get_all_games():
    return jsonify(utils.get_all_games())


@game.route("/games/schema", methods=["GET"])
def get_game_schema():
    return jsonify(utils.get_games_schema())


@game.route("/game/startup/<string:game_name>", methods=["POST"])
def game_startup(game_name):
    game_name_upper = game_name.upper()

    if not _is_supported_game(game_name_upper):
        message = f"/game/startup - {game_name} - is not a suppported game."
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    if game_name_upper == SupportedGameTypes.VRISING.value:
        game = VrisingGame()

    payload = request.json

    if "input_args" in payload.keys():
        input_args = payload["input_args"]

    required_data = game._get_argument_list()

    if not set(required_data).issubset(set(input_args.keys())):
        message = "/game/startup - Error: Missing Required Data"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    for arg_name in input_args.keys():
        game._update_argument(arg_name, input_args[arg_name])

    logger.info("Starting game server")

    # Cannot startup a game that does not exist!
    if not game._is_game_installed():
        message = f"/game/startup - Error: {game_name} is not installed. The user must install first!"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    game.startup()

    return jsonify("Success")


@game.route("/game/shutdown/<string:game_name>", methods=["POST"])
def game_shutdown(game_name):
    game_name_upper = game_name.upper()

    if not _is_supported_game(game_name_upper):
        message = f"/game/startup - {game_name} - is not a suppported game."
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    if game_name_upper == SupportedGameTypes.VRISING.value:
        game = VrisingGame()

    logger.info("Shutting down game server")

    # Cannot shutdown a game that does not exist!
    if not game._is_game_installed():
        message = f"/game/startup - Error: {game_name} is not installed. The user must install first!"
        logger.error(message)
        raise InvalidUsage(message, status_code=400)

    game.shutdown()

    return jsonify("Success")
