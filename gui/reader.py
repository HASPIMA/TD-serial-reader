import serial
from PySide6 import QtCore

from constants import MessageTags


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
        self.status.emit(f"Opening {self.port} @ {self.baud_rate}...")
        try:
            with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
                self.status.emit(f"Listening on {self.port} at {self.baud_rate} baud")
                while self._running:
                    raw = ser.readline()

                    if not raw:
                        continue

                    message = raw.decode("utf-8", errors="replace").strip()

                    if message.startswith(MessageTags.TASK_A):
                        content = message[len(MessageTags.TASK_A) :].strip()
                        self.new_task_a.emit(content)

                    elif message.startswith(MessageTags.TASK_B):
                        content = message[len(MessageTags.TASK_B) :].strip()
                        self.new_task_b.emit(content)

                    else:
                        self.new_unknown.emit(message)

        except serial.SerialException as exc:
            self.status.emit(f"Serial error: {exc}")

    def stop(self) -> None:
        self._running = False
