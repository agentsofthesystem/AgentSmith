from datetime import datetime

from application.extensions import DATABASE


class Games(DATABASE.Model):
    __tablename__ = "games"
    game_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    game_steam_id = DATABASE.Column(DATABASE.Integer, unique=True)
    game_install_dir = DATABASE.Column(DATABASE.String(256))

    game_created = DATABASE.Column(DATABASE.DateTime, default=datetime.utcnow)
    game_last_update = DATABASE.Column(DATABASE.DateTime, default=datetime.utcnow)
