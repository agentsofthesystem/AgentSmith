from flask import jsonify

from application.models.games import Games
from application.models.settings import Settings
from application.models.tokens import Tokens


def get_startup_data():
    startup_data = {}
    game_server_list = {}
    token_list = {}
    settings_list = {}

    # All Games
    all_games = Games.query.all()
    game_server_list = [x.to_dict() for x in all_games]

    # All Active Tokens
    all_active_tokens = Tokens.query.filter_by(token_active=True).all()
    token_list = [x.to_dict() for x in all_active_tokens]

    # All Settings
    all_settings = Settings.query.all()
    settings_list = [x.to_dict() for x in all_settings]

    startup_data = {
        "games": game_server_list,
        "tokens": token_list,
        "settings": settings_list,
    }

    return jsonify(startup_data)
