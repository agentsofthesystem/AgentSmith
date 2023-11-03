from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFileDialog,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtGui import QFont, QFontMetrics

from application.common.constants import FileModes
from operator_client import Operator


class FileSelectWidget(QWidget):
    def __init__(
        self, client: Operator, file_mode: FileModes, parent: QWidget = None
    ) -> None:
        super().__init__(parent)

        self._parent = parent
        self._client = client
        self._file_mode: FileModes = file_mode
        self._selected_path: str = ""

        self.init_ui()

    def init_ui(self):
        self._layout = QHBoxLayout()
        self._path_line_edit = QLineEdit(self)
        self._browse_button = QPushButton("Browse", self)

        self._path_line_edit.textChanged.connect(self._resize_to_content)

        dialog = QFileDialog(self)

        if self._file_mode == FileModes.DIRECTORY:
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
        elif self._file_mode == FileModes.FILE:
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setOption(QFileDialog.ShowDirsOnly, False)

        self._file_select_dialog = dialog

        self._browse_button.clicked.connect(self.handle_button)

        selector_layout = QHBoxLayout()
        selector_layout.addWidget(self._path_line_edit)
        selector_layout.addWidget(self._browse_button)

        self._layout.addLayout(selector_layout)

        self.setLayout(self._layout)

    def get_line_edit(self) -> QLineEdit:
        return self._path_line_edit

    def handle_button(self) -> None:
        if self._file_mode == FileModes.DIRECTORY:
            path = self._file_select_dialog.getExistingDirectory(
                self, "Select Directory"
            )
        elif self._file_mode == FileModes.FILE:
            path, _ = self._file_select_dialog.getOpenFileName(
                self, "Select Path/File", ""
            )

        if path:
            self._path_line_edit.setText(path)

    def _resize_to_content(self):
        text = self._path_line_edit.text()

        # Use QFontMetrics this way;
        font = QFont("", 0)
        fm = QFontMetrics(font)
        pixel_width = fm.width(text)
        pixel_height = fm.height()

        # TODO - Have min pixel width and do not go below it.
        self._path_line_edit.setFixedSize(pixel_width, pixel_height)

        self.adjustSize()
