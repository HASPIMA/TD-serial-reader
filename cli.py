from typing import NoReturn

import serial

from constants import MessageTags


def handle_task_a(message: str):
    print(f"Task A received: {message}")


def handle_task_b(message: str):
    print(f"Task B received: {message}")


def handle_unknown(message: str):
    print(f"Unknown message: {message}")


def entrypoint(
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

            if message.startswith(MessageTags.TASK_A):
                content = message[len(MessageTags.TASK_A) :].strip()
                handle_task_a(content)

            elif message.startswith(MessageTags.TASK_B):
                content = message[len(MessageTags.TASK_B) :].strip()
                handle_task_b(content)

            else:
                handle_unknown(message)
