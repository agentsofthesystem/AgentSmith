from application.extensions import DATABASE
from application.common.pagination import PaginatedApi
from application.common.constants import FileModes


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
    is_permanent = DATABASE.Column(DATABASE.Boolean, nullable=True, default=False)
    file_mode = DATABASE.Column(
        DATABASE.Integer, nullable=True, default=FileModes.NOT_A_FILE.value
    )

    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            field = column.key

            if getattr(self, field) == []:
                continue

            data[field] = getattr(self, field)

        return data
