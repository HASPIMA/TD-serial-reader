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


def main(
    port: str,
    baud_rate: int,
) -> NoReturn:
    with serial.Serial(port, baud_rate, timeout=1) as ser:
        print(f"Listening on {port} at {baud_rate} baud...")

        while True:
            # readline() waits until it receives '\n'
            raw = ser.readline()

            if not raw:
                continue

            message = raw.decode("utf-8", errors="replace").strip()

            if message.startswith(TAG_TASK_A):
                content = message[len(TAG_TASK_A) :].strip()
                handle_task_a(content)

            elif message.startswith(TAG_TASK_B):
                content = message[len(TAG_TASK_B) :].strip()
                handle_task_b(content)

            else:
                handle_unknown(message)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        "serial-reader",
        description="Reader of tasks by serial",
    )

    parser.add_argument(
        "--port",
        "-p",
        type=str,
        default=SERIAL_PORT,
        help="Serial port to read from (e.g: /dev/ttyUSB0)",
    )

    parser.add_argument(
        "--baud-rate",
        "-b",
        type=int,
        default=BAUD_RATE,
        help="Baud rate (e.g: 115200)",
    )

    args = parser.parse_args()

    main(
        port=args.port,
        baud_rate=args.baud_rate,
    )
