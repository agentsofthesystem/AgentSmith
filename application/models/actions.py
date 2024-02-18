from datetime import datetime

from application.extensions import DATABASE
from application.common.pagination import PaginatedApi


class Actions(PaginatedApi, DATABASE.Model):
    __tablename__ = "actions"

    action_id = DATABASE.Column(DATABASE.Integer, primary_key=True)

    game_id = DATABASE.Column(
        DATABASE.Integer, DATABASE.ForeignKey("games.game_id"), nullable=False
    )

    type = DATABASE.Column(DATABASE.String(100), nullable=False)
    result = DATABASE.Column(DATABASE.String(100), nullable=True)
    owner = DATABASE.Column(DATABASE.String(100), nullable=False, default="NONE")
    timestamp = DATABASE.Column(
        DATABASE.DateTime, nullable=False, default=datetime.utcnow
    )
    spare = DATABASE.Column(DATABASE.String(100), nullable=True)

    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            field = column.key

            if getattr(self, field) == []:
                continue

            data[field] = getattr(self, field)

        return data
