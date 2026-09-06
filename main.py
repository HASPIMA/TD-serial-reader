from cli import entrypoint as entrypoint_cli
from constants import ApplicationMode, DeviceConfig
from gui import entrypoint as entrypoint_gui

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

    parser.add_argument(
        "--mode",
        "-m",
        choices=[mode.value for mode in ApplicationMode],
        default=ApplicationMode.GUI,
        help="Whether to run the application in CLI or GUI mode",
    )

    args = parser.parse_args()

    if args.mode == ApplicationMode.CLI:
        entrypoint_cli(
            port=args.port,
            baud_rate=args.baud_rate,
        )
    elif args.mode == ApplicationMode.GUI:
        entrypoint_gui(
            default_port=args.port,
            deafult_baud_rate=args.baud_rate,
        )
