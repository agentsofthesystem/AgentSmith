from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QFrame,
)
from PyQt5.QtGui import QClipboard

from application.common import logger
from operator_client import Operator


class TokensWidget(QWidget):
    def __init__(self, client: Operator, clipboard: QClipboard, parent: QWidget = None):
        super(QWidget, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._client = client
        self._clipboard = clipboard
        self._initialized = False

        self._new_token_name: QLineEdit = None
        self._newly_generated_token: QLineEdit = None
        self._clipboard_copy_button: QPushButton = None

        self._current_tokens: QFrame = None

        self.init_ui()

    def init_ui(self):
        self._layout.addLayout(self._create_generate_token())
        self._layout.addLayout(self._create_newly_generated_token())

        self._current_tokens = self._build_token_frame()
        self._layout.addWidget(self._current_tokens)

        self._newly_generated_token.hide()
        self._clipboard_copy_button.hide()

        self.setFocus()
        self.setLayout(self._layout)
        self.show()

    def _create_generate_token(self) -> QHBoxLayout:
        h_layout = QHBoxLayout()
        self._new_token_name = QLineEdit()
        self._new_token_name.setPlaceholderText("< Enter Token Name >")
        button = QPushButton("Generate")
        button.clicked.connect(self._generate_token)
        h_layout.addWidget(self._new_token_name)
        h_layout.addWidget(button)

        return h_layout

    def _create_newly_generated_token(self) -> QHBoxLayout:
        h_layout = QHBoxLayout()
        self._newly_generated_token = QLineEdit()
        self._clipboard_copy_button = QPushButton("Copy to Clipboard")
        self._clipboard_copy_button.clicked.connect(self._copy_to_clipboard)
        h_layout.addWidget(self._newly_generated_token)
        h_layout.addWidget(self._clipboard_copy_button)

        return h_layout

    def _create_token_entry(self, token_name):
        h_layout = QHBoxLayout()
        label = QLabel(token_name)
        button = QPushButton("Invalidate")
        button.clicked.connect(lambda: self._invalidate_token(token_name))
        h_layout.addWidget(label)
        h_layout.addWidget(button)

        return h_layout

    def _create_tokens_vbox(self) -> QVBoxLayout:
        v_layout = QVBoxLayout()

        all_tokens = self._client.access.get_all_active_tokens()

        if len(all_tokens) == 0:
            v_layout.addWidget(QLabel("No Tokens Yet!"))
        elif len(all_tokens) == 1:
            v_layout.addLayout(self._create_token_entry(all_tokens[0]["token_name"]))
        else:
            for token in all_tokens:
                print(f"Token: name {token['token_name']}")
                h_sep = QFrame()
                h_sep.setFrameShape(QFrame.HLine)
                v_layout.addLayout(self._create_token_entry(token["token_name"]))
                v_layout.addWidget(h_sep)

        return v_layout

    def _build_token_frame(self):
        token_frame = QFrame()
        token_frame.setLayout(self._create_tokens_vbox())
        token_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        token_frame.setLineWidth(1)

        return token_frame

    def _update(self):
        old_token_frame = self._current_tokens
        old_token_frame.hide()
        self._current_tokens = self._build_token_frame()
        self._layout.replaceWidget(old_token_frame, self._current_tokens)

    def _generate_token(self):
        logger.info("Generating token")

        token_name = self._new_token_name.text()

        if token_name == "":
            message = QMessageBox()
            message.setText("Error: Must supply an name for the token. Try again!")
            message.exec()
            return

        token = self._client.access.generate_access_token(token_name)

        logger.debug(f"Token is: {token}")

        if token is False:
            message = QMessageBox()
            message.setText(
                f"Error: Unable to create token. Token named '{token_name}' already exists!"
            )
            message.exec()
            return

        self._newly_generated_token.setText(token)
        self._newly_generated_token.show()
        self._clipboard_copy_button.show()

        self._new_token_name.setText("")  # Set to empty again.

        message = QMessageBox()
        message.setText(
            "Copy Token to safe location. Afterward you will no longer be able to see it."
        )
        message.exec()

        self._new_token_name.setText("")  # Set to empty again.

        self._update()

    def _copy_to_clipboard(self):
        text_for_cb = self._newly_generated_token.text()
        self._clipboard.clear(mode=self._clipboard.Clipboard)
        self._clipboard.setText(text_for_cb, mode=self._clipboard.Clipboard)

        message = QMessageBox()
        message.setText("Text is on clipboard. Paste as needed...")
        message.exec()

        self._newly_generated_token.setText("")
        self._newly_generated_token.hide()
        self._clipboard_copy_button.hide()

    def _invalidate_token(self, token_name):
        logger.debug(f"Invalidating Token: {token_name}")
        self._client.access.invalidate_token(token_name)
        self._update()
