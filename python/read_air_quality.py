#!/usr/bin/env python3
"""Read ENS160 measurements from a USB serial port."""

import argparse
import csv
import json
from pathlib import Path
import sys

import serial
from serial.tools import list_ports

from ens160_serial import ENS160Reading, parse_reading


CSV_FIELDS = list(ENS160Reading.__dataclass_fields__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", help="Serial port, for example COM3 or /dev/ttyACM0")
    parser.add_argument("--baud", type=int, default=9600, help="Serial baud rate (default: 9600)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Read timeout in seconds")
    parser.add_argument("--csv", type=Path, help="Optionally append readings to this CSV file")
    parser.add_argument("--list-ports", action="store_true", help="List serial ports and exit")
    return parser.parse_args()


def print_ports() -> None:
    ports = list(list_ports.comports())
    if not ports:
        print("No serial ports detected.")
        return
    for port in ports:
        print(f"{port.device}\t{port.description}")


def open_csv(path: Path | None):
    if path is None:
        return None, None
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not path.exists() or path.stat().st_size == 0
    handle = path.open("a", newline="", encoding="utf-8")
    writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
    if needs_header:
        writer.writeheader()
        handle.flush()
    return handle, writer


def main() -> int:
    args = parse_args()
    if args.list_ports:
        print_ports()
        return 0
    if not args.port:
        print("error: --port is required unless --list-ports is used", file=sys.stderr)
        return 2

    csv_handle, csv_writer = open_csv(args.csv)
    try:
        with serial.Serial(args.port, args.baud, timeout=args.timeout) as connection:
            print(f"Reading {args.port} at {args.baud} baud. Press Ctrl+C to stop.", file=sys.stderr)
            while True:
                raw_line = connection.readline()
                if not raw_line:
                    continue
                line = raw_line.decode("utf-8", errors="replace").strip()
                reading = parse_reading(line)
                if reading is None:
                    if line:
                        print(f"device: {line}", file=sys.stderr)
                    continue
                data = reading.to_dict()
                print(json.dumps(data), flush=True)
                if csv_writer is not None:
                    csv_writer.writerow(data)
                    csv_handle.flush()
    except KeyboardInterrupt:
        return 0
    except serial.SerialException as error:
        print(f"serial error: {error}", file=sys.stderr)
        return 1
    finally:
        if csv_handle is not None:
            csv_handle.close()


if __name__ == "__main__":
    raise SystemExit(main())
