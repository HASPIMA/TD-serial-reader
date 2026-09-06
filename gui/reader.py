from PySide6 import QtCore


class SerialReaderThread(QtCore.QThread):
    new_task_a = QtCore.Signal(str)
    new_task_b = QtCore.Signal(str)
    new_unknown = QtCore.Signal(str)
    status = QtCore.Signal(str)

    def __init__(
        self,
        port: str,
        baud_rate: int,
        parent: QtCore.QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.port = port
        self.baud_rate = baud_rate
        self._running = True

    def run(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError
