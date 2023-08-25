from datetime import datetime

from application.extensions import DATABASE
from application.common.pagination import PaginatedApi


class GamesArguments(PaginatedApi, DATABASE.Model):
    __tablename__ = "game_arguments"

    game_arg_id = DATABASE.Column(DATABASE.Integer, primary_key=True)

    game_id = DATABASE.Column(
        DATABASE.Integer,
        DATABASE.ForeignKey("games.game_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    game_arg = DATABASE.Column(DATABASE.Integer, unique=True)
    game_arg_value = DATABASE.Column(DATABASE.String(256))

    required = DATABASE.Column(DATABASE.Boolean, nullable=True, default=True)

    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            field = column.key

            if getattr(self, field) == []:
                continue

            data[field] = getattr(self, field)

        return data
