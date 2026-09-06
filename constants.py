from dataclasses import dataclass
from enum import StrEnum, auto, unique


@dataclass(frozen=True)
class DeviceConfig:
    SERIAL_PORT: str = "/dev/ttyUSB0"
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
