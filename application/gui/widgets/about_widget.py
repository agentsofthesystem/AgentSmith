from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from application.common.decorators import timeit
from operator_client import Operator


class AboutWidget(QWidget):
    @timeit
    def __init__(
        self,
        client: Operator,
        parent: QWidget = None,
    ):
        super(QWidget, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._client = client
        self._initialized = False

        self.init_ui()

    def init_ui(self):
        v_layout = QVBoxLayout()

        version = self._client.app.get_app_version()
        q_label = QLabel(f"Software Version: {version}")
        v_layout.addWidget(q_label)

        self._layout.addLayout(v_layout)

        self.setFocus()
        self.setLayout(self._layout)
        self.show()
