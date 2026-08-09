"""Basic RPLIDAR C1 reader (USB serial).

Install:
  pip install rplidar

Usage:
  python basic_rplidar_c1.py --port COM4

This script prints a few (angle, distance_mm) samples from the scan.
"""

from __future__ import annotations

import argparse
import itertools
import sys
import time


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Read scans from SLAMTEC RPLIDAR C1")
    p.add_argument(
        "--port",
        required=False,
        default="COM4",  # <-- placeholder; change to your actual port (e.g. COM3, COM5)
        help="Serial port for the RPLIDAR (Windows: COMx, Linux/macOS: /dev/ttyUSBx).",
    )
    p.add_argument(
        "--baudrate",
        type=int,
        default=115200,
        help="Serial baudrate (default: 115200).",
    )
    p.add_argument(
        "--max-points",
        type=int,
        default=200,
        help="Maximum number of points to print before exiting.",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        from rplidar import RPLidar
    except Exception as e:
        print("Failed to import rplidar. Install with: pip install rplidar", file=sys.stderr)
        raise

    lidar = RPLidar(args.port, baudrate=args.baudrate)

    # Ensure we start streaming
    time.sleep(0.2)

    printed = 0
    try:
        # iter_scans yields scans; each scan is an iterable of (quality, angle, distance).
        for scan in lidar.iter_scans():
            for item in scan:
                # rplidar library usually returns (quality, angle, distance)
                quality, angle_deg, distance_mm = item

                # Print a subset; skip invalid/zero ranges
                if distance_mm <= 0:
                    continue

                print(
                    f"point {printed:04d}: angle={angle_deg:8.2f} deg, distance={distance_mm:8.1f} mm, quality={quality}"
                )
                printed += 1

                if printed >= args.max_points:
                    return 0
    except KeyboardInterrupt:
        return 0
    finally:
        try:
            lidar.stop()
        except Exception:
            pass
        try:
            lidar.disconnect()
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
