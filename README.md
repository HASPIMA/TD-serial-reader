# Task Serial Reader

A small Python application for reading serial data from a device,
identifying task messages by prefix, and dispatching them to either a
CLI handler or a GUI dashboard.

## Table of contents

- [Task Serial Reader](#task-serial-reader)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Building binaries locally](#building-binaries-locally)
  - [Usage](#usage)
    - [CLI mode](#cli-mode)
    - [GUI mode](#gui-mode)
  - [Message format](#message-format)
  - [Notes](#notes)
  - [Example behavior](#example-behavior)

## Overview

This project listens on a configured serial port and reads
newline-terminated messages. Each message is decoded as UTF-8 and
classified according to its tag prefix:

- `[Task A]` → sent to the Task A handler
- `[Task B]` → sent to the Task B handler
- anything else → treated as an unknown or unmatched message

The application can run in two modes:

- CLI mode: reads serial traffic and prints matching messages to the
  terminal
- GUI mode: displays connection state, task data, and unknown traffic
  in separate panels with controls for the serial connection

## Features

- Reads serial data from a configurable port and baud rate
- Filters messages using custom tags from the constants module
- Handles invalid UTF-8 bytes gracefully using replacement decoding
- Provides a terminal-based and desktop-based interface
- Lists available serial ports automatically depending on the host OS
- Suggests matching ports in the GUI with case-insensitive completion
- Reloads the available ports list from the GUI without restarting the app
- Lets users reset connection settings to the defaults in one click
- Shows connection and status updates in the unknown-message panel
- Includes per-panel clear buttons for Task A, Task B, and unknown data
- Builds versioned release binaries for Linux and Windows using GitHub Actions

## Requirements

- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.13 or newer
- `pyserial`
- `PySide6`
- `pyinstaller` (only needed if you want to build packaged release binaries)

## Installation

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Install the project dependencies:

   ```bash
   uv sync
   ```

### Building binaries locally

> [!NOTE]
> This is completely optional and you may not need to build binaries
> if you just want to run the application from source.

1. Install the development tooling, including `pyinstaller`:

   ```bash
   uv sync --all-extras --dev
   ```

2. Build the executable with PyInstaller:

   ```bash
   uv run pyinstaller --clean --onefile --noconsole --name task-serial-reader main.py
   ```

    The binary will be created in the `dist/` directory. On Linux and
    Windows, this produces a standalone executable you can distribute or
    run locally.

3. If you want a console window for CLI mode output, remove
  `--noconsole` from the PyInstaller command.

## Usage

### CLI mode

```bash
uv run main.py --mode cli --port /dev/ttyUSB0 --baud-rate 115200
```

Short aliases are also supported:

```bash
uv run main.py -m cli -p /dev/ttyUSB0 -b 115200
```

In CLI mode, each incoming line is processed as follows:

```text
[Task A] sample task message
```

This is routed to the Task A handler with the message content
`sample task message`.

### GUI mode

```bash
uv run main.py --mode gui --port /dev/ttyUSB0 --baud-rate 115200
```

or:

```bash
uv run main.py -m gui -p /dev/ttyUSB0 -b 115200
```

The GUI lets you:

- choose a serial port from a pre-populated list or type it manually
- use OS-aware serial port discovery to list candidate devices
- reload the list of available ports at any time
- enter a baud rate and reset it to the default values
- connect/disconnect the device and monitor the current state
- view Task A, Task B, and unknown messages in separate sections
- clear each message list individually
- see status updates such as connection attempts and port reload events

## Message format

The application expects newline-delimited messages. For example:

```text
[Task A] Move left motor
[Task B] Read sensor value
```

Messages that do not start with one of the configured tags are treated
as unknown and displayed as-is.

## Notes

- The serial port is opened with a `timeout=1` so the reader loop can
  keep checking for incoming data without blocking indefinitely.
- Incoming raw bytes are decoded with `errors="replace"`, which
  prevents invalid UTF-8 sequences from crashing the application.
- The reader strips trailing newlines and whitespace before matching
  prefixes.
- Port discovery is OS-specific: Windows checks COM ports, Linux
  checks `/dev/tty*`, and macOS checks `/dev/tty.*`.
- The GUI keeps the connection state and displayed details in sync
  with the active serial reader thread.

## Example behavior

When the serial input contains:

```text
[Task A] start job
```

the CLI prints:

```text
Task A received: start job
```

When the serial input contains an unrecognized message, it is routed to
the unknown handler instead and shown in the unknown panel in GUI mode.
