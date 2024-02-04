from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QCheckBox,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QFrame,
    QMessageBox,
)

from PyQt5.QtCore import Qt

from application.common.constants import FileModes
from application.common.decorators import timeit
from application.gui.widgets.file_select_widget import FileSelectWidget
from operator_client import Operator


class AddArgumentWidget(QWidget):
    @timeit
    def __init__(self, client: Operator, parent: QWidget = None) -> None:
        super(QWidget, self).__init__(parent)

        self._parent = parent
        self._client = client
        self._initialized = False
        self._game_name: str = ""

        self._layout = QGridLayout()
        self.setWindowTitle("New Game Argument!")

        self._arg_name_edit: QLineEdit = None
        self._arg_value_edit: QWidget = None
        self._arg_required: QCheckBox = None
        self._arg_file_mode_edit: QComboBox = None
        self._arg_equals_edit: QCheckBox = None
        self._arg_quotes_edit: QCheckBox = None

        self._submit_btn: QPushButton = QPushButton("Submit")
        self._reset_btn: QPushButton = QPushButton("Reset")

    def init_ui(self, game_name: str):
        self._layout.setAlignment(Qt.AlignTop)

        self._layout.addWidget(QLabel("Add Argument:"), 0, 0)

        self._arg_name_edit = QLineEdit()
        self._arg_value_edit = QLineEdit()
        self._arg_required = QCheckBox()
        self._arg_file_mode_edit = QComboBox()
        self._arg_equals_edit = QCheckBox()
        self._arg_quotes_edit = QCheckBox()

        self._arg_file_mode_edit.addItem("Not a File")
        self._arg_file_mode_edit.addItem("File")
        self._arg_file_mode_edit.addItem("Directory")
        self._arg_file_mode_edit.currentTextChanged.connect(self._update_value_edit)

        self._layout.addWidget(QLabel("Argument Name: "), 1, 0)
        self._layout.addWidget(self._arg_name_edit, 1, 1)

        self._layout.addWidget(QLabel("Argument Value: "), 2, 0)
        self._layout.addWidget(self._arg_value_edit, 2, 1)

        self._layout.addWidget(QLabel("Required? "), 3, 0)
        self._layout.addWidget(self._arg_required, 3, 1)

        self._layout.addWidget(QLabel("File Mode Select: "), 4, 0)
        self._layout.addWidget(self._arg_file_mode_edit, 4, 1)

        self._layout.addWidget(QLabel("Use Equals?"), 5, 0)
        self._layout.addWidget(self._arg_equals_edit, 5, 1)

        self._layout.addWidget(QLabel("Use Quotes?"), 6, 0)
        self._layout.addWidget(self._arg_quotes_edit, 6, 1)

        # Separator
        h_sep = QFrame()
        h_sep.setFrameShape(QFrame.HLine)
        self._layout.addWidget(h_sep, 7, 0)

        self._layout.addWidget(self._submit_btn, 8, 0)

        self.setLayout(self._layout)

        self.update(game_name)

        self._initialized = True

    def update(self, game_name: str):
        self._game_name = game_name

        # self._submit_btn.clicked.disconnect()
        self._submit_btn.clicked.connect(lambda: self._submit_argument(game_name))

    def _update_value_edit(self, file_mode_string: str) -> None:
        old_edit_widget = self._arg_value_edit
        old_edit_widget.hide()

        if file_mode_string == "Not a File":
            self._arg_value_edit = QLineEdit()
        elif file_mode_string == "File":
            self._arg_value_edit = FileSelectWidget(self._client, FileModes.FILE)
        elif file_mode_string == "Directory":
            self._arg_value_edit = FileSelectWidget(self._client, FileModes.DIRECTORY)

        self._layout.replaceWidget(old_edit_widget, self._arg_value_edit)
        self.adjustSize()

    def _submit_argument(self, game_name: str) -> None:
        # Line edit
        arg_name = self._arg_name_edit.text()

        # combo
        file_mode = self._arg_file_mode_edit.currentIndex()

        arg_required = self._arg_required.isChecked()
        arg_equals = self._arg_equals_edit.isChecked()
        arg_quotes = self._arg_quotes_edit.isChecked()

        if file_mode == FileModes.NOT_A_FILE.value:
            arg_value = self._arg_value_edit.text()
        elif (
            file_mode == FileModes.FILE.value or file_mode == FileModes.DIRECTORY.value
        ):
            arg_value = self._arg_value_edit.get_line_edit().text()

        argument_id = self._client.game.create_argument(
            game_name,
            arg_name,
            arg_value,
            is_permanent=False,
            required=arg_required,
            file_mode=file_mode,
            use_equals=arg_equals,
            use_quotes=arg_quotes,
        )

        message = QMessageBox()
        if argument_id == -1:
            message.setText("New Arg: There was an error creating the argument.")
        else:
            message.setText("Success!")
            self.hide()

        message.exec()
