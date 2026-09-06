import logging
from typing import Final

from PySide6 import QtCore, QtGui, QtWidgets

from gui.reader import SerialReaderThread


class TasksReaderInterface(QtWidgets.QWidget):
    dev_port: str
    baud_rate: int

    def __init__(
        self,
        *,
        default_port: str,
        default_baud_rate: int,
    ) -> None:
        super().__init__()

        self.default_dev_port: Final[str] = default_port
        self.default_baud_rate: Final[int] = default_baud_rate

        self.dev_port = self.default_dev_port
        self.baud_rate = self.default_baud_rate

        # Top status area
        self.port_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.baud_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        status_layout = QtWidgets.QHBoxLayout()
        status_layout.addWidget(self.port_label)
        status_layout.addWidget(self.baud_label)

        # Two panels side-by-side for Task A and Task B
        self.task_a_list = QtWidgets.QListWidget()
        self.task_b_list = QtWidgets.QListWidget()

        task_a_group = QtWidgets.QGroupBox("Task A Messages")
        task_a_layout = QtWidgets.QVBoxLayout(task_a_group)
        task_a_layout.addWidget(self.task_a_list)

        task_b_group = QtWidgets.QGroupBox("Task B Messages")
        task_b_layout = QtWidgets.QVBoxLayout(task_b_group)
        task_b_layout.addWidget(self.task_b_list)

        middle_layout = QtWidgets.QHBoxLayout()
        middle_layout.addWidget(task_a_group)
        middle_layout.addWidget(task_b_group)

        # Lower panel for unknown messages
        unknown_group = QtWidgets.QGroupBox("Unknown / Unmatched Messages")
        self.unknown_list = QtWidgets.QListWidget()
        unknown_layout = QtWidgets.QVBoxLayout(unknown_group)
        unknown_layout.addWidget(self.unknown_list)

        # Main layout
        self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(status_layout)
        self.layout.addLayout(middle_layout)
        self.layout.addWidget(unknown_group)

        # Set initial labels
        self._update_status_labels(
            f"Port: {self.dev_port}",
            f"Baud: {self.baud_rate}",
        )

        # Start serial reader thread
        self.reader_thread = SerialReaderThread(
            self.dev_port,
            self.baud_rate,
            self,
        )
        self.reader_thread.new_task_a.connect(self._on_new_task_a)
        self.reader_thread.new_task_b.connect(self._on_new_task_b)
        self.reader_thread.new_unknown.connect(self._on_new_unknown)
        self.reader_thread.status.connect(self._on_status)
        self.reader_thread.start()

    def _update_status_labels(self, port_text: str, baud_text: str) -> None:
        self.port_label.setText(port_text)
        self.baud_label.setText(baud_text)

    @QtCore.Slot(str)
    def _on_new_task_a(self, message: str) -> None:
        self.task_a_list.addItem(message)
        self.task_a_list.scrollToBottom()

    @QtCore.Slot(str)
    def _on_new_task_b(self, message: str) -> None:
        self.task_b_list.addItem(message)
        self.task_b_list.scrollToBottom()

    @QtCore.Slot(str)
    def _on_new_unknown(self, message: str) -> None:
        self.unknown_list.addItem(message)
        self.unknown_list.scrollToBottom()

    @QtCore.Slot(str)
    def _on_status(self, text: str) -> None:
        # update baud/port label with latest status message
        self._update_status_labels(
            f"Port: {self.dev_port}",
            f"Baud: {self.baud_rate}",
        )
        # also add to unknown list as a visible status log
        self.unknown_list.addItem(f"[STATUS] {text}")
        self.unknown_list.scrollToBottom()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: N802
        # stop reader thread cleanly
        try:
            if hasattr(self, "reader_thread") and self.reader_thread.isRunning():
                self.reader_thread.stop()
                self.reader_thread.wait(2_000)
        except Exception:
            logging.getLogger(__name__).exception(
                "Failed to stop serial reader thread cleanly",
            )
        super().closeEvent(event)
