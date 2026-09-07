import logging
from collections.abc import Callable
from typing import Final

from PySide6 import QtCore, QtGui, QtWidgets

from constants import ConnectionState
from gui.reader import SerialReaderThread
from utils.serial_ports import list_serial_ports


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
        self.reader_thread: SerialReaderThread | None = None
        self.connection_state: ConnectionState = ConnectionState.DISCONNECTED

        self.dev_port = self.default_dev_port
        self.baud_rate = self.default_baud_rate

        connection_layout = self._setup_connection_layout()
        settings_group = self._setup_settings_group()
        middle_layout, unknown_panel = self._setup_message_panels()

        self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(connection_layout)
        self.layout.addWidget(settings_group)
        self.layout.addLayout(middle_layout)
        self.layout.addWidget(unknown_panel)

        self._update_settings_summary()
        self._set_connection_state(ConnectionState.DISCONNECTED)

    def _setup_connection_layout(self) -> QtWidgets.QHBoxLayout:
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.connection_indicator = QtWidgets.QLabel()
        self.connection_indicator.setFixedSize(14, 14)
        self.connection_indicator.setToolTip("Connection status")

        self.connection_state_label = QtWidgets.QLabel()
        self.connection_state_label.setObjectName("connectionStateLabel")

        self.connection_details_label = QtWidgets.QLabel()
        self.connection_details_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight,
        )

        layout.addWidget(self.connection_indicator)
        layout.addWidget(self.connection_state_label)
        layout.addStretch()
        layout.addWidget(self.connection_details_label)
        return layout

    def _setup_settings_group(self) -> QtWidgets.QGroupBox:
        settings_group = QtWidgets.QGroupBox("Connection Settings")
        settings_layout = QtWidgets.QGridLayout(settings_group)

        self.port_edit = QtWidgets.QComboBox()
        self.port_edit.setEditable(True)
        self.port_edit.setInsertPolicy(
            QtWidgets.QComboBox.InsertPolicy.NoInsert,
        )
        self.port_edit.addItems(list_serial_ports())
        self.port_edit.setCurrentText(self.default_dev_port)
        self.port_edit.editTextChanged.connect(self._update_settings_summary)

        # Allow users to filter by available ports while typing
        self.port_completer = QtWidgets.QCompleter(self.port_edit.model(), self)
        self.port_completer.setCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive,
        )
        self.port_completer.setFilterMode(
            QtCore.Qt.MatchFlag.MatchContains,
        )
        self.port_completer.setCompletionMode(
            QtWidgets.QCompleter.CompletionMode.PopupCompletion,
        )
        self.port_edit.setCompleter(self.port_completer)

        self.reload_ports_button = QtWidgets.QPushButton("Reload ports")
        self.reload_ports_button.clicked.connect(self._reload_serial_ports)

        self.baud_edit = QtWidgets.QLineEdit(str(self.default_baud_rate))
        self.baud_edit.setValidator(QtGui.QIntValidator(1, 4_000_000, self))
        self.baud_edit.textChanged.connect(self._update_settings_summary)

        self.connect_button = QtWidgets.QPushButton("Connect")
        self.connect_button.clicked.connect(self._on_connect_button_clicked)

        self.reset_button = QtWidgets.QPushButton("Reset defaults")
        self.reset_button.clicked.connect(self._reset_to_defaults)

        settings_layout.addWidget(QtWidgets.QLabel("Device port"), 0, 0)
        settings_layout.addWidget(self.port_edit, 0, 1)
        settings_layout.addWidget(QtWidgets.QLabel("Baud rate"), 1, 0)
        settings_layout.addWidget(self.baud_edit, 1, 1)
        settings_layout.addWidget(self.connect_button, 0, 2)
        settings_layout.addWidget(self.reset_button, 1, 2)
        settings_layout.addWidget(self.reload_ports_button, 0, 3, 2, 1)
        return settings_group

    def _setup_message_panels(
        self,
    ) -> tuple[QtWidgets.QHBoxLayout, QtWidgets.QGroupBox]:
        self.task_a_list, task_a_panel = self._build_message_panel(
            "Task A Messages",
            self._clear_task_a,
        )
        self.task_b_list, task_b_panel = self._build_message_panel(
            "Task B Messages",
            self._clear_task_b,
        )
        self.unknown_list, unknown_panel = self._build_message_panel(
            "Unknown / Unmatched Messages",
            self._clear_unknown,
        )

        middle_layout = QtWidgets.QHBoxLayout()
        middle_layout.addWidget(task_a_panel)
        middle_layout.addWidget(task_b_panel)
        return middle_layout, unknown_panel

    def _build_message_panel(
        self,
        title: str,
        clear_callback: Callable[[], None],
    ) -> tuple[QtWidgets.QListWidget, QtWidgets.QGroupBox]:
        list_widget = QtWidgets.QListWidget()

        group = QtWidgets.QGroupBox()
        layout = QtWidgets.QVBoxLayout(group)

        header_layout = QtWidgets.QHBoxLayout()
        header_label = QtWidgets.QLabel(title)
        header_label.setStyleSheet("font-weight: 600;")
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(clear_callback)

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(clear_button)

        layout.addLayout(header_layout)
        layout.addWidget(list_widget)

        return list_widget, group

    def _update_settings_summary(self, *_args: object) -> None:
        self.connection_details_label.setText(
            f"Configured: {self.port_edit.currentText().strip() or '—'} @ "
            f"{self.baud_edit.text().strip() or '—'}",
        )

    def _set_indicator_color(self, color: str) -> None:
        self.connection_indicator.setStyleSheet(
            "border: 1px solid rgba(0, 0, 0, 0.25); "
            "border-radius: 7px; "
            f"background-color: {color};",
        )

    def _set_connection_state(
        self,
        state: ConnectionState,
        details: str | None = None,
    ) -> None:
        self.connection_state = state

        if state == ConnectionState.CONNECTED:
            self._set_indicator_color("#2ecc71")
            self.connection_state_label.setText("Connected")
            self.connect_button.setText("Disconnect")
            self.connect_button.setEnabled(True)
        elif state == ConnectionState.CONNECTING:
            self._set_indicator_color("#f39c12")
            self.connection_state_label.setText("Connecting...")
            self.connect_button.setText("Disconnect")
            self.connect_button.setEnabled(True)
        else:
            self._set_indicator_color("#e74c3c")
            self.connection_state_label.setText("Disconnected")
            self.connect_button.setText("Connect")
            self.connect_button.setEnabled(True)

        if details:
            self.connection_details_label.setText(details)
        else:
            self._update_settings_summary()

    def _read_connection_settings(self) -> tuple[str, int] | None:
        port = self.port_edit.currentText().strip()
        baud_text = self.baud_edit.text().strip()

        if not port:
            self._on_new_unknown("Port cannot be empty")
            self._set_connection_state(ConnectionState.DISCONNECTED)
            return None

        try:
            baud_rate = int(baud_text)
        except ValueError:
            self._on_new_unknown("Baud rate must be a valid integer")
            self._set_connection_state(ConnectionState.DISCONNECTED)
            return None

        if baud_rate <= 0:
            self._on_new_unknown("Baud rate must be greater than zero")
            self._set_connection_state(ConnectionState.DISCONNECTED)
            return None

        return port, baud_rate

    def _start_reader_thread(self) -> None:
        self._stop_reader_thread()

        self.reader_thread = SerialReaderThread(
            self.dev_port,
            self.baud_rate,
            self,
        )
        self.reader_thread.new_task_a.connect(self._on_new_task_a)
        self.reader_thread.new_task_b.connect(self._on_new_task_b)
        self.reader_thread.new_unknown.connect(self._on_new_unknown)
        self.reader_thread.status.connect(self._on_status)
        self.reader_thread.finished.connect(self._on_reader_finished)
        self.reader_thread.start()

    def _stop_reader_thread(self) -> None:
        if self.reader_thread is None:
            return

        if self.reader_thread.isRunning():
            self.reader_thread.stop()
            self.reader_thread.wait(2_000)

        self.reader_thread = None

    def _on_connect_button_clicked(self) -> None:
        if self.connection_state in {
            ConnectionState.CONNECTED,
            ConnectionState.CONNECTING,
        }:
            self._disconnect_device()
            return

        self._connect_device()

    def _connect_device(self) -> None:
        settings = self._read_connection_settings()
        if settings is None:
            return

        self.dev_port, self.baud_rate = settings
        self._update_settings_summary()
        self._set_connection_state(
            ConnectionState.CONNECTING,
            f"Connecting to {self.dev_port} @ {self.baud_rate}...",
        )
        self._start_reader_thread()

    def _disconnect_device(self) -> None:
        if self.reader_thread is None:
            self._set_connection_state(ConnectionState.DISCONNECTED)
            return

        self._set_connection_state(
            ConnectionState.CONNECTING,
            "Disconnecting...",
        )
        self._stop_reader_thread()
        self._set_connection_state(ConnectionState.DISCONNECTED)

    def _reset_to_defaults(self) -> None:
        self.port_edit.setCurrentText(self.default_dev_port)
        self.baud_edit.setText(str(self.default_baud_rate))
        self.dev_port = self.default_dev_port
        self.baud_rate = self.default_baud_rate
        self._update_settings_summary()
        self.unknown_list.addItem("[STATUS] Restored default connection settings")
        self.unknown_list.scrollToBottom()

    def _reload_serial_ports(self) -> None:
        raise NotImplementedError("WIP")

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
        self.unknown_list.addItem(f"[STATUS] {text}")
        self.unknown_list.scrollToBottom()

        if text.startswith("Opening "):
            self._set_connection_state(ConnectionState.CONNECTING, text)
        elif text.startswith("Listening on "):
            self._set_connection_state(ConnectionState.CONNECTED, text)
        elif text.startswith("Serial error:"):
            self._set_connection_state(ConnectionState.DISCONNECTED, text)

    def _on_reader_finished(self) -> None:
        self.reader_thread = None
        if self.connection_state != ConnectionState.DISCONNECTED:
            self._set_connection_state(ConnectionState.DISCONNECTED)

    def _clear_task_a(self) -> None:
        self.task_a_list.clear()

    def _clear_task_b(self) -> None:
        self.task_b_list.clear()

    def _clear_unknown(self) -> None:
        self.unknown_list.clear()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: N802
        try:
            self._stop_reader_thread()
        except Exception:
            logging.getLogger(__name__).exception(
                "Failed to stop serial reader thread cleanly",
            )
        super().closeEvent(event)
