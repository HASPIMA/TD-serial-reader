import sys
from typing import NoReturn

from PySide6 import QtWidgets

from .hello_world import MyWidget


def entrypoint(
    default_port: str,  # noqa: ARG001
    deafult_baud_rate: int,  # noqa: ARG001
) -> NoReturn:
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
