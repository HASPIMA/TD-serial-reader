from cli import entrypoint
from constants import DeviceConfig

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
        default=DeviceConfig.SERIAL_PORT,
        help="Serial port to read from (e.g: /dev/ttyUSB0)",
    )

    parser.add_argument(
        "--baud-rate",
        "-b",
        type=int,
        default=DeviceConfig.BAUD_RATE,
        help="Baud rate (e.g: 115200)",
    )

    args = parser.parse_args()

    entrypoint(
        port=args.port,
        baud_rate=args.baud_rate,
    )
