from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
)
from PyQt5.QtCore import Qt

from application.common import constants
from application.gui.globals import GuiGlobals
from client import Client


class SettingsWidget(QWidget):
    def __init__(self, client: Client, globals: GuiGlobals, parent: QWidget):
        super(QWidget, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._client = client
        self._globals = globals
        self._initialized = False

        self.init_ui()

    def init_ui(self):
        self._layout.setAlignment(Qt.AlignTop)

        h_layout = QHBoxLayout()

        steam_install_dir = self._client.app.get_setting_by_name(
            constants.STARTUP_STEAM_SETTING_NAME
        )
        self._globals._steam_install_path = steam_install_dir

        label = QLabel("Steam Install Path: ")
        text_edit = QLineEdit(self._globals._steam_install_path)
        text_edit.textChanged.connect(self._update_steam_install_path)

        h_layout.addWidget(label)
        h_layout.addWidget(text_edit)

        self._layout.addLayout(h_layout)

        self.setLayout(self._layout)

        self._initialized = True

    def _update_steam_install_path(self, path):
        print(f"New Steam Install Path: {path}")
        # TODO - Check if this is a path and not something garbage.
        self._globals._steam_install_path = path
        self._client.app.update_setting_by_name(
            constants.STARTUP_STEAM_SETTING_NAME, path
        )
