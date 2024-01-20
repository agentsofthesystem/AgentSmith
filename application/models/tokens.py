from application.extensions import DATABASE
from application.common.pagination import PaginatedApi


class Tokens(PaginatedApi, DATABASE.Model):
    __tablename__ = "tokens"
    token_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    token_active = DATABASE.Column(DATABASE.Boolean, nullable=False)
    token_name = DATABASE.Column(DATABASE.String(256), unique=True, nullable=False)
    token_value = DATABASE.Column(DATABASE.String(256), unique=True, nullable=False)

    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            field = column.key

            if getattr(self, field) == []:
                continue

            data[field] = getattr(self, field)

        return data
