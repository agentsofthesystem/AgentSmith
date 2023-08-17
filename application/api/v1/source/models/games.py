from datetime import datetime

from application.extensions import DATABASE
from application.common.pagination import PaginatedApi


class Games(PaginatedApi, DATABASE.Model):
    __tablename__ = "games"
    game_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    game_steam_id = DATABASE.Column(DATABASE.Integer, unique=True)
    game_install_dir = DATABASE.Column(DATABASE.String(256))

    game_pid = DATABASE.Column(DATABASE.Integer, nullable=True)

    game_created = DATABASE.Column(DATABASE.DateTime, default=datetime.utcnow)
    game_last_update = DATABASE.Column(DATABASE.DateTime, default=datetime.utcnow)

    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            field = column.key

            if getattr(self, field) == []:
                continue

            data[field] = getattr(self, field)

        return data
