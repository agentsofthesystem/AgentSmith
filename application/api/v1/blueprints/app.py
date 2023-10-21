import sqlalchemy.exc as exc

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from application.source.models.settings import Settings
from application.common import logger
from application.common.decorators import authorization_required
from application.common.exceptions import InvalidUsage
from application.extensions import DATABASE

app = Blueprint("app", __name__, url_prefix="/v1")


@app.route("/health", methods=["GET"])
def health():
    logger.info("App is alive!")
    return jsonify("Alive")


@app.route("/health/secure", methods=["GET"])
@authorization_required
def health_secure():
    logger.info("App is alive!")
    return jsonify("Alive & Secure")


class SettingsApi(MethodView):
    def __init__(self, model):
        self.model = model

    def _get_setting(self, setting_id: int):
        return self.model.query.filter_by(setting_id=setting_id)

    def _get_setting_by_name(self, setting_name: str):
        return self.model.query.filter_by(setting_name=setting_name)

    def _get_all(self):
        return self.model.query

    def get(self, setting_id=None, setting_name=None):
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 10, type=int), 10000)

        if setting_id:
            qry = self._get_setting(setting_id)
            return jsonify(
                Settings.to_collection_dict(
                    qry, page, per_page, "app.settings", setting_id=setting_id
                )
            )
        elif setting_name:
            qry = self._get_setting_by_name(setting_name)
            return jsonify(
                Settings.to_collection_dict(
                    qry,
                    page,
                    per_page,
                    "app.settings_by_name",
                    setting_name=setting_name,
                )
            )
        else:
            qry = self._get_all()
            return jsonify(
                Settings.to_collection_dict(qry, page, per_page, "app.group_settings")
            )

    def post(self):
        payload = request.json

        if "setting_name" not in payload:
            raise InvalidUsage("Bad Request: Missing Setting Name", status_code=400)
        elif "setting_value" not in payload:
            raise InvalidUsage("Bad Request: Missing Setting Value", status_code=400)

        new_setting = Settings()
        new_setting.setting_name = payload["setting_name"]
        new_setting.setting_value = payload["setting_value"]

        try:
            DATABASE.session.add(new_setting)
            DATABASE.session.commit()
        except exc.DatabaseError as err:
            logger.error(str(err))
            DATABASE.session.rollback()
            return "Cannot add duplicate entry.", 400

        return jsonify({"setting_id": new_setting.setting_id})

    def patch(self, setting_id=None, setting_name=None):
        if setting_id and setting_name is None:
            qry = self._get_setting(setting_id)
        elif setting_name and setting_id is None:
            qry = self._get_setting_by_name(setting_name)

        payload = request.json

        if "setting_name" not in payload:
            raise InvalidUsage("Bad Request: Missing Setting Name", status_code=400)
        elif "setting_value" not in payload:
            raise InvalidUsage("Bad Request: Missing Setting Value", status_code=400)

        qry.update(payload)
        DATABASE.session.commit()

        return "Success"

    def delete(self, setting_id):
        qry = self._get_setting(setting_id)
        DATABASE.session.delete(qry)
        DATABASE.session.commit()
        return "", 204


app.add_url_rule(
    "/settings",
    view_func=SettingsApi.as_view("group_settings", Settings),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/settings/<int:setting_id>",
    view_func=SettingsApi.as_view("settings", Settings),
    defaults={"setting_name": None},
)
app.add_url_rule(
    "/settings/name/<string:setting_name>",
    view_func=SettingsApi.as_view("settings_by_name", Settings),
    defaults={"setting_id": None},
    methods=["GET", "PATCH"],
)
