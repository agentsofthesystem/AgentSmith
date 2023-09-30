from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractScrollArea,
    QHeaderView,
)

from PyQt5.QtCore import Qt

from application.common.constants import FileModes
from application.gui.widgets.file_select_widget import FileSelectWidget
from client import Client


class GameArgumentsWidget(QWidget):
    def __init__(self, client: Client, arg_data: dict, parent: QWidget) -> None:
        super(QWidget, self).__init__(parent)

        self._parent = parent
        self._client = client
        self._layout = QVBoxLayout()
        self._arg_data = arg_data
        self._args_dict: dict = {}

        self.init_ui()

    def init_ui(self):
        self._table = QTableWidget()
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table_layout = QVBoxLayout()
        self._table_layout.addWidget(self._table)

        self._table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        self._update_table()

        self.setLayout(self._table_layout)

        self.show()

    def get_args_dict(self) -> dict:
        return self._args_dict

    def _update_table(self):
        num_rows = len(self._arg_data)
        header_labels = ["Arg Name", "Value", "Required", "Actions"]
        num_cols = len(header_labels)

        self._table.setRowCount(num_rows)
        self._table.setColumnCount(num_cols)

        self._table.setHorizontalHeaderLabels(header_labels)

        for r in range(0, num_rows):
            arg = self._arg_data[r]
            arg_name = arg["game_arg"]
            arg_required = arg["required"]
            arg_value = arg["game_arg_value"]
            file_mode = arg["file_mode"]
            is_permanent = arg["is_permanent"]

            for c in range(0, num_cols):
                if c == 0:
                    self._table.setItem(r, c, QTableWidgetItem(arg_name))
                elif c == 1:
                    value_widget = self._get_file_edit_by_mode(file_mode, arg_value)

                    if (
                        file_mode == FileModes.DIRECTORY.value
                        or file_mode == FileModes.FILE.value
                    ):
                        self._args_dict[arg_name] = value_widget.get_line_edit()
                    else:
                        self._args_dict[arg_name] = value_widget

                    self._table.setCellWidget(r, c, value_widget)
                elif c == 2:
                    required_cb = QCheckBox()
                    required_cb.setChecked(True if arg_required == 1 else False)
                    self._table.setCellWidget(r, c, required_cb)
                else:
                    action_widget = self._get_action_widget(is_permanent)
                    self._table.setCellWidget(r, c, action_widget)

                self._table.horizontalHeader().setSectionResizeMode(
                    c, QHeaderView.ResizeToContents
                )

        self._table.resizeRowsToContents()
        self._table.resizeColumnsToContents()
        self.adjustSize()

    def _get_action_widget(self, is_permanent):
        action_widget = QWidget(self._table)
        action_box = QHBoxLayout()
        action_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        save_button = QPushButton("Save", action_widget)
        action_box.addWidget(save_button)
        delete_button = QPushButton("Delete", action_widget)

        # Don't want to allow somone to delete a permanent argument
        if is_permanent:
            delete_button.setEnabled(False)
            delete_button.setStyleSheet("text-decoration: line-through;")

        action_box.addWidget(delete_button)
        action_widget.setLayout(action_box)

        action_widget.show()

        return action_widget

    def _get_file_edit_by_mode(self, file_mode, arg_value):
        if file_mode == FileModes.FILE.value:
            arg_edit_widget = FileSelectWidget(
                self._client, FileModes.FILE, self._table
            )
            arg_edit_widget.get_line_edit().setText(arg_value)
        elif file_mode == FileModes.DIRECTORY.value:
            arg_edit_widget = FileSelectWidget(
                self._client, FileModes.DIRECTORY, self._table
            )
            arg_edit_widget.get_line_edit().setText(arg_value)
        else:
            arg_edit_widget = QLineEdit(arg_value, self._table)

        arg_edit_widget.show()

        return arg_edit_widget
