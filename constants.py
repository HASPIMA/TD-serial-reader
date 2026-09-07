import sys
from dataclasses import dataclass
from enum import StrEnum, auto, unique


def _default_serial_port() -> str:
    """Return the most common serial port for the current operating system."""
    if sys.platform.startswith("win"):
        return "COM3"
    if sys.platform.startswith("darwin"):
        return "/dev/cu.usbserial"
    return "/dev/ttyUSB0"


@dataclass(frozen=True)
class DeviceConfig:
    SERIAL_PORT: str = _default_serial_port()
    """Serial device port (eg: /dev/ttyUSB0, COM3)"""

    BAUD_RATE: int = 115200


@dataclass(frozen=True)
class MessageTags:
    TASK_A: str = "[Task A]"
    TASK_B: str = "[Task B]"


@unique
class ApplicationMode(StrEnum):
    GUI = auto()
    CLI = auto()


@unique
class ConnectionState(StrEnum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()
