from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QHBoxLayout,
)

from application.common.constants import FileModes
from application.gui.widgets.file_select_widget import FileSelectWidget
from client import Client


class GameArgumentsWidget(QWidget):
    def __init__(self, client: Client, arg_data: dict, parent: QWidget) -> None:
        super().__init__(parent)

        self._parent = parent
        self._client = client
        self._layout = QVBoxLayout()
        self._arg_data = arg_data

        for arg in self._arg_data:
            arg_name = arg["game_arg"]
            arg_required = arg["required"]
            arg_value = arg["game_arg_value"]
            file_mode = arg["file_mode"]
            is_permanent = arg["is_permanent"]

            label_box = QHBoxLayout()
            label_box.addWidget(QLabel(arg_name + ":"))

            arg_box = QHBoxLayout()

            if file_mode == FileModes.FILE.value:
                arg_edit_widget = FileSelectWidget(self._client, FileModes.FILE, self)
                arg_edit_widget.get_line_edit().setText(arg_value)
            elif file_mode == FileModes.DIRECTORY.value:
                arg_edit_widget = FileSelectWidget(
                    self._client, FileModes.DIRECTORY, self
                )
                arg_edit_widget.get_line_edit().setText(arg_value)
            else:
                arg_edit_widget = QLineEdit(arg_value)

            arg_box.addWidget(arg_edit_widget)
            required_cb = QCheckBox()
            required_cb.setChecked(True if arg_required == 1 else False)
            arg_box.addWidget(QLabel("Required: "))
            arg_box.addWidget(required_cb)

            save_button = QPushButton("Save")
            arg_box.addWidget(save_button)
            delete_button = QPushButton("Delete")

            # Don't want to allow somone to delete a permanent argument
            if is_permanent:
                delete_button.setEnabled(False)
                delete_button.setStyleSheet("text-decoration: line-through;")

            arg_box.addWidget(delete_button)

            self._layout.addLayout(label_box)
            self._layout.addLayout(arg_box)

        self.setLayout(self._layout)
        self.show()
