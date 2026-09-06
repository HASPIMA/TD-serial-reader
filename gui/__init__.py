import sys
from typing import NoReturn

from PySide6 import QtWidgets

from .reader import TasksReaderInterface


def entrypoint(
    default_port: str,
    default_baud_rate: int,
) -> NoReturn:
    app = QtWidgets.QApplication([])

    widget = TasksReaderInterface(
        default_port=default_port,
        default_baud_rate=default_baud_rate,
    )
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
