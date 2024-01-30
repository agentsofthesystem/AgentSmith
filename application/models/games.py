from datetime import datetime

from application.extensions import DATABASE
from application.common.constants import GameStates
from application.common.pagination import PaginatedApi


class Games(PaginatedApi, DATABASE.Model):
    __tablename__ = "games"
    game_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    game_steam_id = DATABASE.Column(DATABASE.Integer, unique=True, nullable=False)
    game_install_dir = DATABASE.Column(
        DATABASE.String(256), unique=True, nullable=False
    )
    game_name = DATABASE.Column(DATABASE.String(256), nullable=False)
    game_pretty_name = DATABASE.Column(DATABASE.String(256), nullable=False)

    game_pid = DATABASE.Column(DATABASE.Integer, nullable=True)

    game_created = DATABASE.Column(
        DATABASE.DateTime, default=datetime.utcnow, nullable=False
    )
    game_last_update = DATABASE.Column(
        DATABASE.DateTime, default=datetime.utcnow, nullable=False
    )
    game_state = DATABASE.Column(
        DATABASE.String(25), default=GameStates.NOT_STATE.value, nullable=False
    )

    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            field = column.key

            if getattr(self, field) == []:
                continue

            data[field] = getattr(self, field)

        return data
