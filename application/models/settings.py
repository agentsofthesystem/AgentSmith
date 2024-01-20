from application.extensions import DATABASE
from application.common.pagination import PaginatedApi


class Settings(PaginatedApi, DATABASE.Model):
    __tablename__ = "settings"
    setting_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    setting_name = DATABASE.Column(DATABASE.String(256), unique=True, nullable=False)
    setting_value = DATABASE.Column(DATABASE.String(256), nullable=False)

    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            field = column.key

            if getattr(self, field) == []:
                continue

            data[field] = getattr(self, field)

        return data
