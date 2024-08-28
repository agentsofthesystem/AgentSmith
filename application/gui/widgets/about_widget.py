import requests

from packaging.version import Version
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox, QPushButton

from application.common.decorators import timeit
from operator_client import Operator


class AboutWidget(QWidget):
    RELEASES_URL = "https://api.github.com/repos/agentsofthesystem/agent-smith/releases"
    RELEASE_DL_LINK_FMT = (
        "https://github.com/agentsofthesystem/agent-smith/releases/tag/{tag}"
    )

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
        self._update_check_btn: QPushButton = QPushButton("Check for Update")

        self._latest_version = ""
        self._current_version = ""

        self.q_label_1: QLabel = None
        self.q_label_2: QLabel = None
        self.q_label_3: QLabel = None

        self.init_ui()

    def _check_for_update(self, is_initialize=False) -> None:
        update_available = False
        self._latest_version = self._get_latest_release()
        self._current_version = self._client.app.get_app_version()

        if Version(self._current_version) < Version(self._latest_version):
            update_available = True

        update_available_str = "Yes" if update_available else "No"

        self.q_label_1.setText(f"Software Version: {self._current_version}")
        self.q_label_2.setText(f"Latest Version: {self._latest_version}")
        self.q_label_3.setText(f"Update Available? {update_available_str}")

        if update_available and not is_initialize:
            message = QMessageBox(self)
            message.setWindowTitle("Update Download Link")
            message.setText(
                "<p>Update Available</p>"
                f'<p>Download: <a href="{self.RELEASE_DL_LINK_FMT.format(tag=self._latest_version)}">{self.RELEASE_DL_LINK_FMT.format(tag=self._latest_version)}</a></p>'  # noqa: E501
            )
            message.exec()

    def _get_latest_release(self) -> str:
        latest_version = None
        response = requests.get(self.RELEASES_URL)

        if response.status_code == 200:
            output = response.json()
            version_list = [x["tag_name"] for x in output]

        if len(version_list) > 0:
            latest_version = version_list[0]

        return latest_version

    def init_ui(self):
        v_layout = QVBoxLayout()

        self._update_check_btn.clicked.connect(lambda: self._check_for_update())

        self.q_label_1 = QLabel(f"Software Version: {self._current_version}")
        self.q_label_2 = QLabel(f"Latest Version: {self._latest_version}")
        self.q_label_3 = QLabel("Update Available? ")

        v_layout.addWidget(self.q_label_1)
        v_layout.addWidget(self.q_label_2)
        v_layout.addWidget(self.q_label_3)
        v_layout.addWidget(self._update_check_btn)

        self._layout.addLayout(v_layout)

        self._check_for_update(is_initialize=True)

        self.setFocus()
        self.setLayout(self._layout)
        self.show()
