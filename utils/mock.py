import os
import pty
import termios
import time


def main() -> None:
    master_fd, slave_fd = pty.openpty()
    slave_name = os.ttyname(slave_fd)

    # Configure the PTY for 115200 baud, 8N1.
    attrs = termios.tcgetattr(slave_fd)
    """
    Based on https://docs.python.org/3/library/termios.html#termios.tcgetattr :
        attrs[0]: input flags
        attrs[1]: output flags
        attrs[2]: control flags (serial format/options)
        attrs[3]: local flags
        attrs[4]: input speed (input baud rate)
        attrs[5]: output speed (output baud rate)
        attrs[6]: special characters
    """

    """
    This sets 8N1 (More info here: https://www.modemhelp.net/faqs/8n1.shtml)

    Clear several bits in the control flags:
        `CSIZE` -> We clear the mask controlling the data bits
        `PARENB` -> No parity
        `CSTOPB` -> 1 Stop bit

    Set the data bits:
        `CS8`: Use 8 data bits

    This results in:
        8 data bits
        No parity
        1 stop bit

    a.k.a 8N1
    """
    attrs[2] &= ~(termios.PARENB | termios.CSTOPB | termios.CSIZE)
    attrs[2] |= termios.CS8

    """
    Disable hardware flow control

    Without hardware control, the setup is effectively:

        TX ----> RX

    rather than having additional RTS/CTS signaling.
    """
    attrs[2] &= ~termios.CRTSCTS

    # Enable receiving and ignore modem control
    attrs[2] |= termios.CREAD | termios.CLOCAL

    # Set input and output speeds to 115200
    attrs[4] = termios.B115200
    attrs[5] = termios.B115200

    # Apply the configuration immediately (115200 8N1)
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
