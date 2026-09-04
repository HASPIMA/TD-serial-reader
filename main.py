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


def main():
    print("Hello from serial-reader!")


if __name__ == "__main__":
    main()
