import os
import pty
import termios
import time


def main() -> None:
    master_fd, slave_fd = pty.openpty()
    slave_name = os.ttyname(slave_fd)

    # Configure the PTY for 115200 baud, 8N1.
    attrs = termios.tcgetattr(slave_fd)
    attrs[2] &= ~(termios.PARENB | termios.CSTOPB | termios.CSIZE)
    attrs[2] |= termios.CS8
    attrs[2] &= ~termios.CRTSCTS
    attrs[2] |= termios.CREAD | termios.CLOCAL
    attrs[4] = termios.B115200
    attrs[5] = termios.B115200

    termios.tcsetattr(slave_fd, termios.TCSANOW, attrs)

    print(f"Mock serial device at: {slave_name}")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            os.write(master_fd, b"[Task A] message from A\n")
            time.sleep(1)

            os.write(master_fd, b"[Task B] message from B\n")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        os.close(master_fd)
        os.close(slave_fd)


if __name__ == "__main__":
    main()
