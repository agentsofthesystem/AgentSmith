from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QFrame,
    QLayout,
)
from PyQt5.QtGui import QClipboard

from application.managers.nginx_manager import NginxManager


class NginxCertViewer(QMainWindow):
    def __init__(
        self,
        clipboard: QClipboard,
        nginx_manager: NginxManager,
    ):
        super().__init__()

        self.title = "Current SSL Pub Key"

        self._layout = QVBoxLayout()
        self._clipboard = clipboard
        self._nginx_manager = nginx_manager
        self._initialized = False

        self._cert_text = QTextEdit()
        self._cert_text.setDisabled(True)

        self._copy_to_clipboard: QPushButton = QPushButton("Copy")
        self._copy_to_clipboard.clicked.connect(self._handle_copy_button)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)

        self._main_widget = QWidget(self)

        # Get file....
        qframe = QFrame()
        qframe.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        qframe.setLineWidth(1)

        self.update_text_box()

        h_box = QHBoxLayout()
        h_box.addWidget(self._cert_text)
        h_box.addWidget(self._copy_to_clipboard)

        qframe.setLayout(h_box)

        self._layout.addWidget(qframe)

        self._main_layout = QVBoxLayout()
        self._main_layout.addLayout(self._layout)
        self._main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self._main_widget.setLayout(self._main_layout)

        self.setCentralWidget(self._main_widget)

        self.adjustSize()

    def update_text_box(self):
        cert_text = self._nginx_manager.get_public_key_content()

        if cert_text is None:
            self._cert_text.setText("Cert File Does Not Exist.")
        else:
            self._cert_text.setText(cert_text)

    def showWindow(self):
        self.show()

    def _handle_copy_button(self):
        text_for_cb = self._cert_text.toPlainText()
        self._clipboard.clear(mode=self._clipboard.Clipboard)
        self._clipboard.setText(text_for_cb, mode=self._clipboard.Clipboard)

        message = QMessageBox()
        message.setText("Text is on clipboard. Paste as needed...")
        message.exec()
