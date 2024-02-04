from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QTabWidget,
)
from PyQt5.QtCore import Qt

from application.common import constants, logger
from application.common.decorators import timeit
from application.gui.globals import GuiGlobals
from application.gui.widgets.file_select_widget import FileSelectWidget
from application.gui.widgets.nginx_widget import NginxWidget
from application.gui.widgets.tokens_widget import TokensWidget
from application.managers.nginx_manager import NginxManager
from operator_client import Operator


class SettingsWidget(QWidget):
    @timeit
    def __init__(self, client: Operator, globals: GuiGlobals, parent: QWidget = None):
        super(QWidget, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._client = client
        self._globals = globals
        self._initialized = False

        self._token_widget = TokensWidget(
            self._client,
            self._globals._global_clipboard,
            parent=self,
            init_data=self._globals._init_tokens_data,
        )
        self._nginx_manager: NginxManager = self._globals._nginx_manager

        self._nginx_widget = NginxWidget(
            self._client,
            self._globals._global_clipboard,
            self._nginx_manager,
            parent=self,
            init_data=self._globals._init_settings_data,
        )

        self.setWindowTitle("App Settings")

    def init_ui(self):
        self._layout.setAlignment(Qt.AlignTop)

        steam_install_dir = self._globals._init_settings_data[
            constants.SETTING_NAME_STEAM_PATH
        ]
        default_install_dir = self._globals._init_settings_data[
            constants.SETTING_NAME_DEFAULT_PATH
        ]

        # Add back in later if needed - Comment out for now.
        # application_secret = self._globals._init_settings_data[constants.SETTING_NAME_APP_SECRET]

        self._globals._steam_install_path = steam_install_dir

        self.tabs = QTabWidget()

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        tab1_layout = QVBoxLayout()
        tab1_layout.addLayout(self._create_steam_path_setting(steam_install_dir))
        tab1_layout.addLayout(
            self._create_default_install_path_setting(default_install_dir)
        )
        self.tab1.setLayout(tab1_layout)

        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(self._token_widget)

        # TODO - Disabling for now. Add back in later if needed.
        # tab2_layout.addLayout(self._create_app_secret_setting(application_secret))

        self.tab2.setLayout(tab2_layout)

        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(self._nginx_widget)
        self.tab3.setLayout(tab3_layout)

        self.tabs.addTab(self.tab1, "Paths")
        self.tabs.addTab(self.tab2, "Tokens")
        self.tabs.addTab(self.tab3, "Nginx")

        self._layout.addWidget(self.tabs)

        self.setLayout(self._layout)

        self.setFocus()

        self._initialized = True

    def _create_steam_path_setting(self, steam_install_dir: str) -> QHBoxLayout:
        h_layout1 = QHBoxLayout()
        label1 = QLabel("Steam Install Path: ")
        text_edit1 = FileSelectWidget(self._client, constants.FileModes.DIRECTORY, self)
        text_edit1.get_line_edit().setText(steam_install_dir)
        text_edit1.get_line_edit().textChanged.connect(self._update_steam_install_path)
        h_layout1.addWidget(label1)
        h_layout1.addWidget(text_edit1)

        return h_layout1

    def _create_default_install_path_setting(
        self, defaut_install_dir: str
    ) -> QHBoxLayout:
        h_layout1 = QHBoxLayout()
        label1 = QLabel("Default Install Path: ")
        text_edit1 = FileSelectWidget(self._client, constants.FileModes.DIRECTORY, self)
        text_edit1.get_line_edit().setText(defaut_install_dir)
        text_edit1.get_line_edit().textChanged.connect(
            self._update_default_install_path
        )
        h_layout1.addWidget(label1)
        h_layout1.addWidget(text_edit1)

        return h_layout1

    def _create_app_secret_setting(self, application_secret: str) -> QHBoxLayout:
        h_layout2 = QHBoxLayout()
        label2 = QLabel("Application Secret: ")
        text_edit2 = QLineEdit()
        text_edit2.setText(application_secret)
        text_edit2.textChanged.connect(self._update_app_secret)
        h_layout2.addWidget(label2)
        h_layout2.addWidget(text_edit2)

        return h_layout2

    def _update_steam_install_path(self, path):
        logger.info(f"New Steam Install Path: {path}")
        # TODO - Check if this is a path and not something garbage.
        self._globals._steam_install_path = path
        self._client.app.update_setting_by_name(constants.SETTING_NAME_STEAM_PATH, path)

    def _update_default_install_path(self, path):
        logger.info(f"New Default Install Path: {path}")
        # TODO - Check if this is a path and not something garbage.
        self._globals._default_install_path = path
        self._client.app.update_setting_by_name(
            constants.SETTING_NAME_DEFAULT_PATH, path
        )

    def _update_app_secret(self, text):
        # TODO - Changing the app secret invalidates all existing tokens.
        # Need to add a save button and then prompt the user that changing the secrent
        # invalidates all other existing tokens.  If they "save" then delete all of them.
        self._client.app.update_setting_by_name(constants.SETTING_NAME_APP_SECRET, text)
