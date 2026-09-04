from typing import NoReturn

import serial

SERIAL_PORT = "/dev/ttyUSB0"  # Change to COM3 on Windows, for example
BAUD_RATE = 115200

TAG_TASK_A = "[Task A]"
TAG_TASK_B = "[Task B]"


def handle_task_a(message: str):
    print(f"Task A received: {message}")


def handle_task_b(message: str):
    print(f"Task B received: {message}")


def handle_unknown(message: str):
    print(f"Unknown message: {message}")


def main() -> NoReturn:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud...")

        while True:
            # readline() waits until it receives '\n'
            raw = ser.readline()

            if not raw:
                continue

            message = raw.decode("utf-8", errors="replace").strip()

            if message.startswith(TAG_TASK_A):
                content = message[len(TAG_TASK_A):].strip()
                handle_task_a(content)

            elif message.startswith(TAG_TASK_B):
                content = message[len(TAG_TASK_B):].strip()
                handle_task_b(content)

            else:
                handle_unknown(message)


if __name__ == "__main__":
    main()
