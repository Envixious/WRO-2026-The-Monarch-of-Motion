#!/usr/bin/env python3
"""Diagnostic script to test serial connection with ESP32."""

from __future__ import annotations

import argparse
import time
from serial_utils import get_available_ports
import serial


def test_serial_connection(port: str, baud: int = 9600, test_duration: float = 5.0) -> bool:
    """Test if the serial port can open and send data."""
    print(f"[test] Attempting to open {port} @ {baud} baud...")
    try:
        ser = serial.Serial(port, baud, timeout=0.1)
        print(f"[test] ✓ Successfully opened {port}")
    except Exception as exc:
        print(f"[test] ✗ Failed to open {port}: {exc}")
        return False

    print(f"[test] Testing communication for {test_duration} seconds...")
    print(f"[test] Sending forward command: 0,50")

    try:
        start = time.time()
        count = 0
        while time.time() - start < test_duration:
            msg = "0,50\n"
            ser.write(msg.encode("ascii"))
            count += 1
            time.sleep(0.1)
        
        print(f"[test] ✓ Sent {count} forward commands successfully")
        print(f"[test] Sending stop command: 0,0")
        ser.write("0,0\n".encode("ascii"))
        ser.close()
        return True
    except Exception as exc:
        print(f"[test] ✗ Communication failed: {exc}")
        try:
            ser.close()
        except Exception:
            pass
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Test serial connection to ESP32 chassis")
    parser.add_argument(
        "--port",
        default=None,
        help="Serial port (e.g., /dev/ttyS2, /dev/ttyUSB0, COM3). Auto-detect if not specified.",
    )
    parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")
    parser.add_argument("--duration", type=float, default=5.0, help="Test duration in seconds")
    args = parser.parse_args()

    print("[test] Serial Connection Diagnostic")
    print("=" * 50)

    available = get_available_ports()
    if available:
        print(f"[test] Available serial ports: {', '.join(available)}")
    else:
        print("[test] No serial ports detected!")

    port = args.port
    if not port:
        if available:
            port = available[0]
            print(f"[test] Using first available port: {port}")
        else:
            print("[test] ERROR: No ports available and no --port specified")
            return 1

    success = test_serial_connection(port, args.baud, args.duration)

    print("=" * 50)
    if success:
        print("[test] ✓ Serial connection test PASSED")
        print(f"[test] Run: python fusion_main.py --serial-port {port} --serial-baudrate {args.baud}")
        return 0
    else:
        print("[test] ✗ Serial connection test FAILED")
        print("[test] Possible issues:")
        print("  - Wrong serial port (try other available ports above)")
        print("  - Wrong baud rate (check ESP32 firmware)")
        print("  - USB cable not connected")
        print("  - Permissions issue on Linux/Orange Pi (try 'sudo')")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
