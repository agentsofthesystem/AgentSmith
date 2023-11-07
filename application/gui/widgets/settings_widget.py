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
from application.gui.globals import GuiGlobals
from application.gui.widgets.file_select_widget import FileSelectWidget
from application.gui.widgets.tokens_widget import TokensWidget
from operator_client import Operator


class SettingsWidget(QWidget):
    def __init__(self, client: Operator, globals: GuiGlobals, parent: QWidget = None):
        super(QWidget, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._client = client
        self._globals = globals
        self._initialized = False

        self._token_widget = TokensWidget(
            self._client, self._globals._global_clipboard, self
        )

        self.setWindowTitle("App Settings")

    def init_ui(self):
        self._layout.setAlignment(Qt.AlignTop)

        steam_install_dir = self._client.app.get_setting_by_name("steam_install_dir")
        application_secret = self._client.app.get_setting_by_name("application_secret")
        self._globals._steam_install_path = steam_install_dir

        self.tabs = QTabWidget()

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        tab1_layout = QVBoxLayout()
        tab1_layout.addLayout(self._create_steam_path_setting(steam_install_dir))
        tab1_layout.addLayout(self._create_app_secret_setting(application_secret))
        self.tab1.setLayout(tab1_layout)

        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(self._token_widget)
        self.tab2.setLayout(tab2_layout)

        self.tabs.addTab(self.tab1, "Settings")
        self.tabs.addTab(self.tab2, "Tokens")

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
        self._client.app.update_setting_by_name("steam_install_dir", path)

    def _update_app_secret(self, text):
        # TODO - Changing the app secret invalidates all existing tokens.
        self._client.app.update_setting_by_name("application_secret", text)
