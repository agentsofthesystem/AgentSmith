import sqlalchemy.exc as exc

from enum import Enum
from flask import Blueprint, request, jsonify
from flask.views import MethodView

from application.common import logger, toolbox
from application.common.constants import FileModes
from application.common.exceptions import InvalidUsage
from application.extensions import DATABASE
from application.source.games.vrising_game import VrisingGame
from application.source.models.games import Games
from application.source.models.game_arguments import GamesArguments

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
    return jsonify(toolbox.get_all_games())


@game.route("/games/schema", methods=["GET"])
def get_game_schema():
    return jsonify(toolbox.get_games_schema())


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


class GameArguments(MethodView):
    def __init__(self, model):
        self.model = model

    def _get_argument(self, game_arg_id: int):
        return self.model.query.filter_by(game_arg_id=game_arg_id)

    def _get_game_id(self, game_name: str):
        gobj = Games.query.filter_by(game_name=game_name).first()
        return gobj.game_id

    def _get_argument_by_name(self, game_name: str, argument_name: str):
        return self.model.query.filter_by(
            game_id=self._get_game_id(game_name), game_arg=argument_name
        )

    def _get_all(self):
        return self.model.query

    def get(self, game_name=None, game_arg_id=None, argument_name=None):
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 10, type=int), 10000)

        if game_arg_id:
            qry = self._get_argument(game_arg_id)
            return jsonify(
                GamesArguments.to_collection_dict(
                    qry, page, per_page, "game.arguments", game_arg_id=game_arg_id
                )
            )
        elif argument_name:
            qry = self._get_argument_by_name(game_name, argument_name)
            return jsonify(
                GamesArguments.to_collection_dict(
                    qry,
                    page,
                    per_page,
                    "game.game_arguments_by_name",
                    game_name=game_name,
                    argument_name=argument_name,
                )
            )
        else:
            qry = self._get_all()
            return jsonify(
                GamesArguments.to_collection_dict(
                    qry, page, per_page, "game.group_arguments"
                )
            )

    def post(self):
        payload = request.json

        if "game_arg" not in payload:
            raise InvalidUsage("Bad Request: Missing Argument Name", status_code=400)
        if "game_arg_value" not in payload:
            raise InvalidUsage("Bad Request: Missing Argument Value", status_code=400)
        if "game_name" not in payload:
            raise InvalidUsage(
                "Bad Request: Missing Game Name to associate with", status_code=400
            )

        try:
            game_id = self._get_game_id(payload["game_name"])
        except AttributeError:
            raise InvalidUsage(
                f"Bad Request: Game Name {payload['game_name']} does not exist!",
                status_code=400,
            )

        new_argument = GamesArguments()
        new_argument.game_arg = payload["game_arg"]
        new_argument.game_arg_value = payload["game_arg_value"]
        new_argument.game_id = game_id

        if "required" in payload:
            new_argument.required = payload["required"]

        if "is_permanent" in payload:
            new_argument.required = payload["is_permanent"]

        if "file_mode" in payload:
            mode = int(payload["file_mode"])
            if mode == FileModes.FILE.value:
                new_argument.file_mode = FileModes.FILE.value
            elif mode == FileModes.DIRECTORY.value:
                new_argument.file_mode = FileModes.DIRECTORY.value
            elif mode == FileModes.NOT_A_FILE.value:
                new_argument.file_mode = FileModes.NOT_A_FILE.value
            else:
                raise InvalidUsage(
                    "Bad Request: Invalid File Mode Provied!", status_code=400
                )

        try:
            DATABASE.session.add(new_argument)
            DATABASE.session.commit()
        except exc.DatabaseError as err:
            logger.error(str(err))
            DATABASE.session.rollback()
            return "Cannot add duplicate entry.", 400

        return jsonify({"game_arg_id": new_argument.game_arg_id})

    def patch(self, game_name=None, game_arg_id=None, argument_name=None):
        if game_arg_id and argument_name is None:
            qry = self._get_argument(game_arg_id)
        elif argument_name and game_arg_id is None:
            qry = self._get_argument_by_name(game_name, argument_name)

        payload = request.json

        if "game_arg" not in payload:
            raise InvalidUsage("Bad Request: Missing Argument Name", status_code=400)
        if "game_arg_value" not in payload:
            raise InvalidUsage("Bad Request: Missing Argument Value", status_code=400)

        qry.update(payload)
        DATABASE.session.commit()

        return "Success"

    def delete(self, game_arg_id):
        qry = self._get_argument(game_arg_id)
        DATABASE.session.delete(qry)
        DATABASE.session.commit()
        return "", 204


game.add_url_rule(
    "/game/arguments",
    view_func=GameArguments.as_view("group_arguments", GamesArguments),
    methods=["GET", "POST"],
)
game.add_url_rule(
    "/game/argument/<int:game_arg_id>",
    view_func=GameArguments.as_view("arguments", GamesArguments),
    defaults={"argument_name": None},
)
game.add_url_rule(
    "/game/<string:game_name>/argument/<string:argument_name>",
    view_func=GameArguments.as_view("game_arguments_by_name", GamesArguments),
    defaults={"game_arg_id": None},
    methods=["GET", "PATCH"],
)
