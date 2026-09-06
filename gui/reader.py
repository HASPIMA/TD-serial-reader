from typing import Final

from PySide6 import QtCore, QtWidgets


class TasksReaderInterface(QtWidgets.QWidget):
    def __init__(
        self,
        *,
        default_port: str,
        default_baud_rate: int,
    ) -> None:
        super().__init__()

        self.default_dev_port: Final[str] = default_port
        self.default_baud_rate: Final[int] = default_baud_rate

        self.serial_port_text = QtWidgets.QLabel(
            f"Listening to serial port: {self.default_dev_port}",
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.serial_port_text)
