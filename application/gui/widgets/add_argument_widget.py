import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from PyQt5.QtCore import Qt

from application.common.constants import FileModes
from client import Client


class AddArgumentWidget(QWidget):
    def __init__(self, client: Client, game_name: str, parent: QWidget = None) -> None:
        super(QWidget, self).__init__(parent)

        self._parent = parent
        self._client = client
        self._game_name = game_name
        self._initialized = False
        self._layout = QVBoxLayout()
        self.setWindowTitle("App Settings")

    def init_ui(self):
        self._layout.setAlignment(Qt.AlignTop)

        h_layout = QHBoxLayout()

        temp_label = QLabel("Add Args Widget!!!")

        h_layout.addWidget(temp_label)

        self._layout.addLayout(h_layout)

        self.setLayout(self._layout)

        self._initialized = True
