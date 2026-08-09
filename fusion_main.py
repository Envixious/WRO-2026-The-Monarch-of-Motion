"""Main fusion decision engine for RPLIDAR C1 + PixyCam2 + Chassis.

Behaviour:
  1. Read PixyCam2 detections (green / red / pink / orange / blue colour blobs).
  2. If multiple colours are detected simultaneously, use the LiDAR
     to measure distance to each and pick the closest colour.
  3. Act based on the winning colour:
       Green  -> turn right (regular corner)
       Red    -> turn left (regular corner)
       Pink   -> execute parallel park routine
       Orange -> forced 90-deg turn LEFT (straight ending, must turn)
       Blue   -> forced 90-deg turn RIGHT (track ending, must turn)
  4. If no colour is detected, stop the car.

Run:
  python fusion_main.py --lidar-port COM4
"""

from __future__ import annotations

import argparse
import signal
import sys
import time
from typing import List, Optional, Tuple

from chassis_control import Chassis
from lidar_reader import LidarReader
from parallel_park import parallel_park
from pixy_reader import PixyReader

PIXY_FOV_DEG = 60


def _pixy_x_to_angle(x: int) -> float:
    """Convert PixyCam2 pixel x to angle offset from centre (degrees)."""
    normalised = (x - 159.5) / 159.5
    return normalised * (PIXY_FOV_DEG / 2.0)


def _resolve_colour_with_lidar(
    detections: list,
    lidar: LidarReader,
) -> Optional[str]:
    """If multiple colours, pick the one closest via LiDAR."""
    if not detections:
        return None
    if len(detections) == 1:
        return detections[0].color

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


def _perform_90_turn(
    chassis: Chassis,
    direction: str,
    speed: float = 0.3,
    turn_time: float = 1.5,
) -> None:
    """Execute a hard 90-degree turn, then resume going straight.

    Parameters
    ----------
    direction : "left" or "right"
    speed     : motor speed during the turn (0.0 - 1.0)
    turn_time : approximate time to achieve 90 degrees (tune for your chassis)
    """
    if direction == "left":
        print(f"[action] ORANGE -> 90-degree turn LEFT")
        chassis.turn_left(speed=speed)
    else:
        print(f"[action] BLUE -> 90-degree turn RIGHT")
        chassis.turn_right(speed=speed)

    time.sleep(turn_time)
    print("[action] Resuming straight")
    chassis.forward(speed=speed)
    time.sleep(0.5)
    chassis.stop()


def _colour_action(
    colour: str,
    chassis: Chassis,
    lidar: LidarReader,
) -> None:
    """Perform action for a colour."""
    if colour == "red":
        print("[action] RED -> turn LEFT")
        chassis.turn_left(speed=0.3)
        time.sleep(0.8)
        chassis.forward(speed=0.3)
        time.sleep(1.0)
        chassis.stop()

    elif colour == "green":
        print("[action] GREEN -> turn RIGHT")
        chassis.turn_right(speed=0.3)
        time.sleep(0.8)
        chassis.forward(speed=0.3)
        time.sleep(1.0)
        chassis.stop()

    elif colour == "pink":
        print("[action] PINK -> parallel park")
        parallel_park(chassis, lidar, speed=0.3, timeout=20.0)

    elif colour == "orange":
        # Forced 90-degree left turn when straight is about to end
        _perform_90_turn(chassis, "left", speed=0.3, turn_time=1.5)

    elif colour == "blue":
        # Forced 90-degree right turn when track is about to end
        _perform_90_turn(chassis, "right", speed=0.3, turn_time=1.5)

    else:
        print(f"[action] Unknown colour '{colour}'")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fusion engine: PixyCam2 + RPLIDAR + Chassis"
    )
    parser.add_argument("--lidar-port", default="COM4")
    parser.add_argument("--lidar-baudrate", type=int, default=115200)
    parser.add_argument("--action-cooldown", type=float, default=2.0)
    parser.add_argument(
        "--turn-time",
        type=float,
        default=1.5,
        help="Approx seconds for a 90-degree turn (tune for your chassis)",
    )
    args = parser.parse_args()

    print("[fusion] Initialising LiDAR...")
    lidar = LidarReader(port=args.lidar_port, baudrate=args.lidar_baudrate)
    lidar.start()

    print("[fusion] Initialising PixyCam2...")
    pixy = PixyReader()
    pixy.start()

    print("[fusion] Initialising Chassis...")
    chassis = Chassis()

    shutdown_requested = False

    def _signal_handler(sig, frame):
        nonlocal shutdown_requested
        shutdown_requested = True

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    last_action_time = 0.0
    last_noise_print = 0.0
    print("[fusion] Fusion engine running. Ctrl+C to stop.")

    try:
        while not shutdown_requested:
            detections = pixy.get_detected_colors()
            colours_present = [d.color for d in detections]
            selected_colour = _resolve_colour_with_lidar(detections, lidar)
            now = time.monotonic()

            if selected_colour and (now - last_action_time >= args.action_cooldown):
                print(f"[fusion] Colours: {colours_present} -> Selected: {selected_colour}")
                last_action_time = now
                _colour_action(selected_colour, chassis, lidar)

            elif not selected_colour:
                if now - last_noise_print >= 1.0:
                    print("[fusion] No colour detected")
                    last_noise_print = now
                chassis.stop()

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        print("\n[fusion] Shutting down...")
        chassis.stop()
        chassis.cleanup()
        pixy.stop()
        lidar.stop()
        print("[fusion] Done.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
