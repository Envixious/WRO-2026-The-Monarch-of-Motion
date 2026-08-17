"""Main fusion decision engine for RPLIDAR C1 + PixyCam2 + Chassis.

Behaviour:
  1. Read PixyCam2 detections (green / red / pink / orange / blue colour blobs).
  2. If multiple colours are detected simultaneously, use the LiDAR
     to measure distance to each and pick the closest colour.
  3. Act based on the winning colour:
       Green  -> turn right (regular corner)
       Red    -> turn left (regular corner)
       Pink   -> execute parallel park routine
  4. If no colour is detected, stop the car.

Run:
  python fusion_main.py --lidar-port /DEV/TTYUSB0
"""

from __future__ import annotations

import argparse
import os
import pickle
import signal
import subprocess
import sys
import time
from typing import List, Optional, Tuple
from serial_chassis import SerialChassis as Chassis
from parallel_park import parallel_park
from pixy_reader import PixyReader
from serial_utils import get_available_ports

PIXY_FOV_DEG = 60
LIDAR_DATA_PATH = os.environ.get("LIDAR_DATA_PATH", "/dev/shm/lidar.data")
SAFE_STOP_MM = 500
MIN_CLEARANCE_MM = 300  # Minimum space required to confidently turn toward that side


class LidarProxy:
    """Small adapter that reads the shared pickle written by scan_lidar.py.
    
    Uses per-iteration snapshot caching to avoid repeated file I/O in the hot loop.
    Call refresh_snapshot() once per main loop iteration for optimal performance.
    """

    def __init__(self, snapshot_path: str = LIDAR_DATA_PATH) -> None:
        self._snapshot_path = snapshot_path
        self._cached_snapshot = None  # Cache for current iteration
        self._snapshot_timestamp = 0.0

    def refresh_snapshot(self) -> None:
        """Load snapshot once per main loop iteration. Call at start of loop."""
        self._cached_snapshot = _load_lidar_snapshot(self._snapshot_path)
        self._snapshot_timestamp = time.time()

    def is_available(self) -> bool:
        # If no cached snapshot yet, try to load once
        if self._cached_snapshot is None:
            self.refresh_snapshot()
        return self._cached_snapshot is not None

    def get_distance_at(self, angle: float) -> Optional[float]:
        # Use cached snapshot (already loaded by refresh_snapshot)
        if self._cached_snapshot is None:
            return None
        idx = int(round(angle)) % 360
        return self._cached_snapshot.get(idx)

    def get_obstacles_in_sector(
        self,
        start_angle: float,
        end_angle: float,
        max_distance: float = 1000.0,
    ) -> List[Tuple[float, float]]:
        # Use cached snapshot (already loaded by refresh_snapshot)
        if self._cached_snapshot is None:
            return []

        start_i = int(round(start_angle)) % 360
        end_i = int(round(end_angle)) % 360
        results: List[Tuple[float, float]] = []

        if start_i <= end_i:
            angles = range(start_i, end_i + 1)
        else:
            angles = list(range(start_i, 360)) + list(range(0, end_i + 1))

        for angle in angles:
            distance = self._cached_snapshot.get(angle)
            if distance is not None and distance > 0 and distance < max_distance:
                results.append((float(angle), float(distance)))

        return results

    def get_output_file_path(self) -> str:
        return self._snapshot_path


def _load_lidar_snapshot(path: Optional[str] = None) -> Optional[dict]:
    """Load the latest LiDAR scan snapshot from the shared pickle file."""
    snapshot_path = path or LIDAR_DATA_PATH
    if not snapshot_path or not os.path.exists(snapshot_path):
        return None

    try:
        with open(snapshot_path, "rb") as handle:
            return pickle.load(handle)
    except Exception:
        return None


def _pixy_x_to_angle(x: int) -> float:
    """Convert PixyCam2 pixel x to angle offset from centre (degrees)."""
    normalised = (x - 159.5) / 159.5
    return normalised * (PIXY_FOV_DEG / 2.0)


def _is_too_close(lidar: Optional[object], threshold_mm: int = SAFE_STOP_MM) -> bool:
    """Return True only when the true front-center path is blocked.

    The robot should keep using PixyCam steering while the front is still clear.
    LiDAR override begins only when the obstacle is very close to the straight-ahead
    path, not merely off to the side.
    """
    if lidar is None or not lidar.is_available():
        return False

    front_angles = list(range(350, 360)) + list(range(0, 11))
    front_distances = []
    for angle in front_angles:
        dist = lidar.get_distance_at(angle)
        if dist is not None and dist > 0:
            front_distances.append(dist)

    if not front_distances:
        return False

    return min(front_distances) <= threshold_mm


def _sector_clearance(
    lidar: Optional[object],
    start_angle: float,
    end_angle: float,
    max_distance_mm: float = 12000.0,
) -> float:
    """Return the nearest obstacle distance in a sector, or max_distance if clear."""
    if lidar is None or not lidar.is_available():
        return 0.0

    sector = lidar.get_obstacles_in_sector(start_angle, end_angle, max_distance=max_distance_mm)
    if not sector:
        return max_distance_mm

    return min(distance for _, distance in sector)


def _choose_open_side(lidar: Optional[object], min_clearance_mm: int = MIN_CLEARANCE_MM) -> Optional[str]:
    """Choose the side with the most clear space when the front is blocked.

    The LiDAR angle convention used here is: 0° is straight ahead, and the angle
    increases clockwise from the front. That means the left side is the 225°-315°
    sector and the right side is the 45°-135° sector.

    Returns the direction with at least min_clearance_mm of confirmed free space,
    or None if both sides are blocked or unclear.
    """
    if lidar is None or not lidar.is_available():
        return None

    # Left side relative to the vehicle is restricted to the 260°-280° sector.
    left_clearance = _sector_clearance(lidar, 260.0, 280.0)
    # Right side relative to the vehicle is restricted to the 80°-100° sector.
    right_clearance = _sector_clearance(lidar, 80.0, 100.0)

    left_confident = left_clearance >= min_clearance_mm
    right_confident = right_clearance >= min_clearance_mm

    if left_confident and right_confident:
        return "left" if left_clearance >= right_clearance else "right"
    elif left_confident:
        return "left"
    elif right_confident:
        return "right"
    else:
        return None


def _resolve_colour_with_lidar(
    detections: list,
    lidar: Optional[object],
) -> Optional[str]:
    """If multiple colours, pick the one closest via LiDAR."""
    if not detections:
        return None
    if len(detections) == 1:
        return detections[0].color
    if lidar is None or not lidar.is_available():
        return None

    colour_distances: List[Tuple[str, float]] = []
    for det in detections:
        angle = _pixy_x_to_angle(det.x)
        dist = lidar.get_distance_at(int(round(angle % 360)))
        if dist is None or dist <= 0:
            dist = 9999.0
        colour_distances.append((det.color, float(dist)))

    colour_distances.sort(key=lambda cd: cd[1])
    chosen = colour_distances[0][0]
    print(f"[resolve] Closest colour: {chosen} ({colour_distances[0][1]:.0f} mm)")
    return chosen


def _colour_action(
    colour: str,
    chassis,
    lidar: object,
) -> None:
    """Perform action for a colour with proper timing.
    
    Uses timing within the action itself to avoid blocking the main loop.
    """
    if colour == "red":
        print("[action] RED -> turn LEFT")
        chassis.turn_left(30)
        time.sleep(0.8)
        chassis.forward(30)
        time.sleep(1.0)
        chassis.stop()

    elif colour == "green":
        print("[action] GREEN -> turn RIGHT")
        chassis.turn_right(30)
        time.sleep(0.8)
        chassis.forward(30)
        time.sleep(1.0)
        chassis.stop()

    elif colour == "pink":
        print("[action] PINK -> parallel park")
        parallel_park(chassis, lidar, speed=30, timeout=20.0)

    else:
        print(f"[action] Unknown colour '{colour}'")

 
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fusion engine: PixyCam2 + RPLIDAR + Chassis"
    )
    parser.add_argument("--lidar-port", default="/dev/ttyUSB0")
    parser.add_argument("--lidar-baudrate", type=int, default=115200)
    parser.add_argument("--serial-port", default="/dev/ttyS2", help="Serial port for the ESP32 chassis (default: /dev/ttyS2)")
    parser.add_argument("--serial-baudrate", type=int, default=9600)
    parser.add_argument("--action-cooldown", type=float, default=2.0)
    parser.add_argument(
        "--turn-time",
        type=float,
        default=3.0,
        help="Approx seconds for a 90-degree turn (tune for your chassis)",
    )
    parser.add_argument(
        "--min-clearance",
        type=int,
        default=MIN_CLEARANCE_MM,
        help="Minimum clearance (mm) required to turn toward a side (default: %(default)s)",
    )
    args = parser.parse_args()

    if args.min_clearance != MIN_CLEARANCE_MM:
        print(f"[fusion] Using custom min-clearance: {args.min_clearance} mm")

    print("[fusion] Initialising LiDAR helpers...")
    workspace_root = os.path.dirname(os.path.abspath(__file__))
    scan_script = os.path.join(workspace_root, "scan_lidar.py")
    read_script = os.path.join(workspace_root, "read_lidar.py")

    scan_process = None
    read_process = None
    try:
        scan_process = subprocess.Popen(
            [sys.executable, scan_script],
            cwd=workspace_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Output read_lidar to terminal with line buffering (minimal blocking)
        read_process = subprocess.Popen(
            [sys.executable, "-u", read_script],  # -u enables unbuffered output
            cwd=workspace_root,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except Exception as exc:
        print(f"[fusion] Unable to start LiDAR helper scripts: {exc}")

    lidar = LidarProxy(snapshot_path=LIDAR_DATA_PATH)

    print("[fusion] Initialising PixyCam2...")
    pixy = PixyReader()
    pixy.start()
    if not pixy.available:
        print("[fusion] PixyCam2 is unavailable; continuing without camera input.")

    print("[fusion] Initialising Chassis...")
    from serial_chassis import SerialChassis

    try:
        chassis = SerialChassis(port=args.serial_port, baud=args.serial_baudrate)
        print(f"[fusion] Chassis connected on {args.serial_port} @ {args.serial_baudrate} baud")
        chassis.forward(30)
        print("[fusion] Sent initial forward command")
    except Exception as exc:
        available = get_available_ports()
        print(f"[fusion] ERROR: Failed to initialize chassis on {args.serial_port}: {exc}")
        if available:
            print(f"[fusion] Available serial ports: {', '.join(available)}")
            print(f"[fusion] Try: python fusion_main.py --serial-port {available[0]}")
        else:
            print("[fusion] No serial ports detected. Check USB/serial connections.")
        raise

    shutdown_requested = False

    def _signal_handler(sig, frame):
        nonlocal shutdown_requested
        shutdown_requested = True

    def _stop_lidar_helpers() -> None:
        nonlocal scan_process, read_process
        for process in (read_process, scan_process):
            if process is None:
                continue
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=2)
                except Exception:
                    process.kill()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    last_action_time = 0.0
    last_noise_print = 0.0
    lidar_override_active = False
    lidar_override_side = None
    lidar_override_until = 0.0
    print("[fusion] Fusion engine running. Press Ctrl+C to stop both sensors and exit.")

    try:
        while not shutdown_requested:
            # Load LiDAR snapshot ONCE per iteration (avoids repeated file I/O)
            lidar.refresh_snapshot()

            now = time.monotonic()  # Use monotonic clock consistently
            detections = pixy.get_detected_colors()
            colours_present = [d.color for d in detections]

            # Explicit LiDAR override: once the obstacle-avoidance turn starts,
            # Pixy steering is suspended until the override window expires.
            if lidar_override_active:
                if now >= lidar_override_until:
                    print("[fusion] LiDAR override complete; resuming PixyCam steering")
                    pixy.set_lamp(False)
                    chassis.stop()
                    chassis.forward(30)
                    lidar_override_active = False
                    lidar_override_side = None
                    lidar_override_until = 0.0
                    last_noise_print = now
                    time.sleep(0.05)
                    continue

                if lidar_override_side == "left":
                    chassis.turn_left(100, 35)
                    pixy.set_lamp(True)
                elif lidar_override_side == "right":
                    chassis.turn_right(100, 35)
                    pixy.set_lamp(True)
                else:
                    chassis.stop()

                time.sleep(0.05)
                continue

            if not pixy.available:
                if _is_too_close(lidar):
                    if now - last_noise_print >= 1.0:
                        print("[fusion] Obstacle too close; stopping before contact")
                        last_noise_print = now
                    chassis.stop()
                    time.sleep(0.05)
                    continue

                if now - last_noise_print >= 1.0:
                    print("[fusion] PixyCam2 unavailable; maintaining forward motion")
                    last_noise_print = now
                chassis.forward(30)
                time.sleep(0.05)
                continue

            if _is_too_close(lidar):
                open_side = _choose_open_side(lidar, args.min_clearance)
                if open_side == "left":
                    print("[fusion] Front blocked; left side clearer -> LiDAR override turn LEFT")
                    lidar_override_side = "left"
                    lidar_override_until = now + args.turn_time
                    lidar_override_active = True
                    pixy.set_lamp(True)
                    chassis.turn_left(100, 35)
                elif open_side == "right":
                    print("[fusion] Front blocked; right side clearer -> LiDAR override turn RIGHT")
                    lidar_override_side = "right"
                    lidar_override_until = now + args.turn_time
                    lidar_override_active = True
                    pixy.set_lamp(True)
                    chassis.turn_right(100, 35)
                else:
                    print("[fusion] Front blocked; stopping before contact")
                    pixy.set_lamp(False)
                    chassis.stop()
                    time.sleep(0.05)
                    continue

                time.sleep(0.05)
                continue

            selected_colour = _resolve_colour_with_lidar(detections, lidar)

            if selected_colour and (now - last_action_time >= args.action_cooldown):
                print(f"[fusion] Colours: {colours_present} -> Selected: {selected_colour}")
                last_action_time = now
                _colour_action(selected_colour, chassis, lidar)

            elif not selected_colour:
                if now - last_noise_print >= 1.0:
                    print("[fusion] No colour detected; maintaining forward motion")
                    last_noise_print = now
                chassis.forward(30)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("[fusion] User requested shutdown.")
    finally:
        print("\n[fusion] Shutting down...")
        chassis.stop()
        chassis.cleanup()
        pixy.stop()
        _stop_lidar_helpers()
        print("[fusion] Done.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
