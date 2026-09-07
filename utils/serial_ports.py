# Source - https://stackoverflow.com/a/14224477
# Posted by tfeldmann, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-06, License - CC BY-SA 3.0

import glob
import sys

import serial


def list_serial_ports() -> tuple[str, ...]:
    """
    Lists serial port names.

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A tuple of the serial ports available on the system
    """
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")  # noqa: PTH207
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")  # noqa: PTH207
    else:
        raise EnvironmentError("Unsupported platform")  # noqa: UP024

    result: list[str] = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return tuple(result)


if __name__ == "__main__":
    print(list_serial_ports())
