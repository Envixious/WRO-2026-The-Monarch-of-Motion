"""Parallel parking routine for a 2WD RWD car.

Uses the LiDAR to detect the gap, then executes the parking manoeuvre.
The car is 30 cm long x 20 cm wide.

Algorithm (simplified 3-point turn):
  1. Pull up alongside the gap until the front passes the first obstacle.
  2. Full steering lock toward the kerb while reversing slowly.
  3. Straighten wheels and reverse until the rear is in.
  4. Pull forward to centre.

All movements are open-loop with LiDAR checks for obstacle proximity.
"""

from __future__ import annotations

import time
from typing import Optional, Tuple

from chassis_control import Chassis
from lidar_reader import LidarReader


CAR_LENGTH_MM = 300   # 30 cm
CAR_WIDTH_MM  = 200   # 20 cm
SAFE_GAP_MM   = 500   # minimum gap to attempt parking
KERB_SIDE     = 90    # angle at which kerb is expected (left side)


def parallel_park(
    chassis: Chassis,
    lidar: LidarReader,
    speed: float = 0.3,
    timeout: float = 15.0,
) -> bool:
    """Execute a parallel parking manoeuvre.

    Args:
        chassis: Chassis controller (already initialised).
        lidar: LiDAR reader (already started).
        speed: Movement speed (0.0-1.0).
        timeout: Maximum duration in seconds.

    Returns:
        True if parking completed, False on timeout / failure.
    """
    start_time = time.monotonic()

    # ---------- Step 1: Check gap is large enough ----------
    left_dist = lidar.get_distance_at(KERB_SIDE)
    if left_dist and left_dist < SAFE_GAP_MM:
        print(f"[park] Gap too small ({left_dist:.0f} mm), aborting.")
        return False

    # ---------- Step 2: Pull forward past the front obstacle ----------
    # We drive forward until the front of the car is past the obstacle.
    # The obstacle should be on the left (kerb side).
    print("[park] Step 2: Pulling forward past front obstacle...")
    obstacle_clear = False
    for _ in range(50):  # max ~5 seconds of forward movement
        if time.monotonic() - start_time > timeout:
            print("[park] Timeout during forward phase.")
            chassis.stop()
            return False

        # Check if we've passed the obstacle by looking at front-left
        front_left = lidar.get_obstacles_in_sector(30, 60, max_distance=1000)
        if not front_left:
            obstacle_clear = True
            break

        chassis.forward(speed=speed * 0.6)
        time.sleep(0.1)

    chassis.stop()
    time.sleep(0.3)

    if not obstacle_clear:
        print("[park] Could not clear front obstacle.")
        return False

    # ---------- Step 3: Reverse with full left turn ----------
    # This is the "back-in" part of parallel parking.
    print("[park] Step 3: Reversing and turning into space...")
    reverse_start = time.monotonic()
    while time.monotonic() - reverse_start < 3.0:
        if time.monotonic() - start_time > timeout:
            print("[park] Timeout during reverse phase.")
            chassis.stop()
            return False

        # Turn left while reversing -> right wheel forward, left wheel reverse
        # (spin_left reverses left and drives right forward = tank turn left)
        chassis.spin_left(speed=speed)
        time.sleep(0.5)

        # Check if we're about to hit something behind us
        rear = lidar.get_obstacles_in_sector(150, 210, max_distance=400)
        if rear:
            print(f"[park] Obstacle behind ({rear[0][1]:.0f} mm), stopping reverse.")
            break

    chassis.stop()
    time.sleep(0.3)

    # ---------- Step 4: Straighten up by pulling forward ----------
    print("[park] Step 4: Straightening up...")
    straight_start = time.monotonic()
    while time.monotonic() - straight_start < 2.0:
        if time.monotonic() - start_time > timeout:
            break

        # Check front clearance
        front = lidar.get_obstacles_in_sector(0, 30, max_distance=300)
        if front:
            print(f"[park] Obstacle ahead ({front[0][1]:.0f} mm), stopping.")
            break

        chassis.forward(speed=speed * 0.5)
        time.sleep(0.1)

    # ---------- Step 5: Final adjustment ----------
    chassis.stop()
    time.sleep(0.2)

    # Small reverse to centre
    chassis.backward(speed=speed * 0.3)
    time.sleep(0.3)
    chassis.stop()

    print("[park] Parallel parking complete.")
    return True


if __name__ == "__main__":
    # Quick standalone test
    with Chassis() as car:
        lidar = LidarReader(port="COM4")
        lidar.start()
        try:
            print("Testing parallel park routine...")
            success = parallel_park(car, lidar, speed=0.3)
            print(f"Result: {'Success' if success else 'Failed'}")
        finally:
            lidar.stop()
