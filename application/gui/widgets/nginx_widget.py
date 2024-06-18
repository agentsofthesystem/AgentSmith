from PyQt5.QtWidgets import (
    QWidget,
    QCheckBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtGui import QClipboard

from application.common import constants
from application.common.decorators import timeit
from application.gui.widgets.nginx_cert_viewer_widget import NginxCertViewer
from application.managers.nginx_manager import NginxManager

from operator_client import Operator


class NginxWidget(QWidget):
    @timeit
    def __init__(
        self,
        client: Operator,
        clipboard: QClipboard,
        nginx_manager: NginxManager,
        parent: QWidget = None,
        init_data=None,
    ):
        super(QWidget, self).__init__(parent)

        self._layout = QVBoxLayout()
        self._client = client
        self._clipboard = clipboard
        self._nginx_manager = nginx_manager
        self._init_data = init_data
        self._initialized = False

        self._nginx_enable_checkbox: QCheckBox = None
        self._nginx_hostname: QLineEdit = None
        self._nginx_port: QLineEdit = None
        self._nginx_port_save_btn: QPushButton = None
        self._regenerate_certificate: QPushButton = None
        self._view_public_cert: QPushButton = None

        self._viewer_window = NginxCertViewer(self._clipboard, self._nginx_manager)

        self.MIN_PORT_NUMBER = 10000
        self.MAX_PORT_NUMBER = 65535

        self.init_ui()

    def init_ui(self):
        self._layout.addLayout(self._create_nginx_controls())

        self.setFocus()
        self.setLayout(self._layout)
        self.show()

    def _create_nginx_controls(self) -> QVBoxLayout:
        v_control_layout = QVBoxLayout()

        # Nginx Enable / Disable
        h_layout = QHBoxLayout()
        label = QLabel("Nginx On/Off")
        self._nginx_enable_checkbox = QCheckBox()

        is_running = self._nginx_manager.is_running()

        if is_running:
            self._nginx_enable_checkbox.setChecked(True)

        self._nginx_enable_checkbox.toggled.connect(self._handle_nginx_enable_checkbox)

        h_layout.addWidget(label)
        h_layout.addWidget(self._nginx_enable_checkbox)

        # Port / Host / Other Settings
        if self._init_data:
            nginx_proxy_port = self._init_data[constants.SETTING_NGINX_PROXY_PORT]
            nginx_proxy_hostname = self._init_data[
                constants.SETTING_NGINX_PROXY_HOSTNAME
            ]
        else:
            nginx_proxy_port = self._client.app.get_setting_by_name(
                constants.SETTING_NGINX_PROXY_PORT
            )
            nginx_proxy_hostname = self._client.app.get_setting_by_name(
                constants.SETTING_NGINX_PROXY_HOSTNAME
            )

        h2_layout = QHBoxLayout()
        label = QLabel("Nginx Hostname: ")
        self._nginx_hostname = QLineEdit(nginx_proxy_hostname)

        self._nginx_hostname.textChanged.connect(self._handle_nginx_hostname_edit)
        h2_layout.addWidget(label)
        h2_layout.addWidget(self._nginx_hostname)

        h3_layout = QHBoxLayout()
        label = QLabel("Nginx Port: ")
        self._nginx_port = QLineEdit(nginx_proxy_port)
        self._nginx_port_save_btn = QPushButton("Save")

        self._nginx_port_save_btn.clicked.connect(self._handle_nginx_port_save_btn)

        h3_layout.addWidget(label)
        h3_layout.addWidget(self._nginx_port)
        h3_layout.addWidget(self._nginx_port_save_btn)

        self._regenerate_certificate = QPushButton("Reset SSL Certificate")
        self._regenerate_certificate.clicked.connect(self._handle_regen_button)

        self._view_public_cert = QPushButton("View Public Key CRT File")
        self._view_public_cert.clicked.connect(self._handle_view_cert_button)

        v_control_layout.addLayout(h_layout)
        v_control_layout.addLayout(h2_layout)
        v_control_layout.addLayout(h3_layout)

        v_control_layout.addWidget(self._regenerate_certificate)
        v_control_layout.addWidget(self._view_public_cert)

        # Don't let someone edit the settings when nginx is running.
        if is_running:
            self._disable_controls()

        return v_control_layout

    def _enable_controls(self):
        self._nginx_port.setDisabled(False)
        self._nginx_hostname.setDisabled(False)
        self._regenerate_certificate.setDisabled(False)

    def _disable_controls(self):
        self._nginx_port.setDisabled(True)
        self._nginx_hostname.setDisabled(True)
        self._regenerate_certificate.setDisabled(True)

    def _handle_nginx_enable_checkbox(self):
        cbutton = self.sender()
        is_enabled = True if cbutton.isChecked() else False
        self._client.app.update_setting_by_name(
            constants.SETTING_NGINX_ENABLE, is_enabled
        )

        if is_enabled:
            if not self._nginx_manager.is_running():
                self._nginx_manager.startup()
                self._disable_controls()
        else:
            self._nginx_manager.shutdown()
            self._enable_controls()

    def _handle_nginx_hostname_edit(self, text):
        if "http://" in text or "https://" in text:  # covers http and https
            message = QMessageBox()
            message.setText(
                "Enter only the DNS hostname and leave off http:// or https://"
            )
            message.exec()
            return

        self._client.app.update_setting_by_name(
            constants.SETTING_NGINX_PROXY_HOSTNAME, text
        )

    def _handle_nginx_port_save_btn(self):
        text = self._nginx_port.text()
        num_chars = len(text)

        if int(text) <= self.MIN_PORT_NUMBER:
            message = QMessageBox()
            message.setText("Please use a port number greater than 10000.")
            message.exec()
            return

        if int(text) > self.MAX_PORT_NUMBER:
            message = QMessageBox()
            message.setText("Please use a port number less than 65535.")
            message.exec()
            return

        # Make sure every character is a unicode digit.
        if len(text) > len(set(text)):
            message = QMessageBox()
            message.setText("Please make sure all digits in the port are unique.")
            message.exec()
            return

        if num_chars >= 5:
            self._client.app.update_setting_by_name(
                constants.SETTING_NGINX_PROXY_PORT, text
            )

    def _handle_regen_button(self):
        if self._nginx_manager.key_pair_exists():
            self._nginx_manager.remove_ssl_key_pair()

        self._nginx_manager.generate_ssl_certificate()

        message = QMessageBox()
        message.setText("Nginx SSL Self Sign Cert Regenerated.")
        message.exec()

    def _handle_view_cert_button(self):
        self._viewer_window.update_text_box()
        self._viewer_window.showWindow()
