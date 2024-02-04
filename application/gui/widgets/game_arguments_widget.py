from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
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

from application.common import logger
from application.common.constants import FileModes
from application.gui.widgets.file_select_widget import FileSelectWidget
from operator_client import Operator


class GameArgumentsWidget(QWidget):
    ARG_NAME_COL = 0
    ARG_VALUE_COL = 1
    ARG_REQUIRED_COL = 2
    ARG_ACTION_COL = 3

    def __init__(
        self, client: Operator, arg_data: dict, parent: QWidget, disable_cols: list = []
    ) -> None:
        super(QWidget, self).__init__(parent)

        self._parent = parent
        self._client = client
        self._layout = QVBoxLayout()
        self._arg_data = arg_data
        self._args_dict: dict = {}
        self._disable_cols = disable_cols

        self.init_ui()

    def init_ui(self):
        self._table = QTableWidget()
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table_layout = QVBoxLayout()
        self._table_layout.addWidget(self._table)

        self._table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        self.update_arguments_table()

        self.setLayout(self._table_layout)

        self.show()

    def get_args_dict(self) -> dict:
        return self._args_dict

    def disable_scroll_bars(self):
        self.disable_horizontal_scroll()
        self.disable_vertical_scroll()

    def disable_horizontal_scroll(self):
        self._table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def disable_vertical_scroll(self):
        self._table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def update_arguments_table(self, game_arguments=None):
        # Allow argument data to be updated by external caller.
        if game_arguments:
            self._arg_data = game_arguments

        num_rows = len(self._arg_data)

        header_labels = ["Arg Name", "Value", "Required", "Actions"]

        if len(self._disable_cols) > 0:
            if "Required" in self._disable_cols:
                header_labels.remove("Required")
            if "Actions" in self._disable_cols:
                header_labels.remove("Actions")

        num_cols = len(header_labels)

        self._table.setRowCount(0)  # Reset
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

            # When using this widget on the New game Widget, args come from class obj, not database.
            if "game_arg_id" in arg:
                arg_id = arg["game_arg_id"]
            else:
                arg_id = -1

            # Value widget for the given row
            value_widget = None

            # TODO - This works... but its not built very well and can break.
            # If someone disables required but not actions then c == 3 will equal the
            # self._ARG_ACTIONS_COL but its hard coded to 4.  Change it to go back and hide the
            # columns later.
            for c in range(0, num_cols):
                if c == self.ARG_NAME_COL:
                    self._table.setItem(r, c, QTableWidgetItem(arg_name))
                elif c == self.ARG_VALUE_COL:
                    value_widget = self._get_file_edit_by_mode(file_mode, arg_value)

                    if (
                        file_mode == FileModes.DIRECTORY.value
                        or file_mode == FileModes.FILE.value
                    ):
                        self._args_dict[arg_name] = value_widget.get_line_edit()
                    else:
                        self._args_dict[arg_name] = value_widget

                    self._table.setCellWidget(r, c, value_widget)
                elif c == self.ARG_REQUIRED_COL:
                    if "Required" in self._disable_cols:
                        continue
                    required_cb = QCheckBox()
                    required_cb.setChecked(True if arg_required == 1 else False)
                    self._table.setCellWidget(r, c, required_cb)
                elif c == self.ARG_ACTION_COL:
                    if "Actions" in self._disable_cols:
                        continue
                    action_widget = self._get_action_widget(
                        is_permanent, arg_id, arg_name
                    )
                    self._table.setCellWidget(r, c, action_widget)

                self._table.horizontalHeader().setSectionResizeMode(
                    c, QHeaderView.ResizeToContents
                )

        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.resizeRowsToContents()
        self._table.resizeColumnsToContents()
        self.adjustSize()

    def _get_action_widget(self, is_permanent: bool, arg_id: str, arg_name: str):
        action_widget = QWidget(self._table)
        action_box = QHBoxLayout()
        action_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        save_button = QPushButton("Save", action_widget)
        delete_button = QPushButton("Delete", action_widget)

        save_button.clicked.connect(lambda: self._update_argument(arg_id, arg_name))
        delete_button.clicked.connect(lambda: self._delete_argument(arg_id))

        action_box.addWidget(save_button)

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
            arg_edit_widget = QLineEdit(str(arg_value), self._table)

        arg_edit_widget.show()

        return arg_edit_widget

    def _delete_argument(self, arg_id):
        logger.debug(f"Deleting Argument id: {arg_id}!")

        message = QMessageBox()

        if self._client.game.delete_argument_by_id(arg_id):
            message.setText("Argument Deleted.")
        else:
            message.setText("Error: Argument not deleted...")
        message.exec()

    def _update_argument(self, arg_id, arg_name):
        logger.debug(f"Updating Argument id: {arg_id}!")

        value_widget = self._args_dict[arg_name]
        if isinstance(value_widget, FileSelectWidget):
            new_arg_value = value_widget.get_line_edit().text()
        else:
            new_arg_value = value_widget.text()

        message = QMessageBox()

        if self._client.game.update_argument_by_id(arg_id, new_arg_value):
            message.setText(f"Updated Argument: {arg_name} to: {new_arg_value}.")
        else:
            message.setText("Error: Argument not updated...")
        message.exec()
