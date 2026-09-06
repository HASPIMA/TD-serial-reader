from typing import Final

from PySide6 import QtWidgets


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
