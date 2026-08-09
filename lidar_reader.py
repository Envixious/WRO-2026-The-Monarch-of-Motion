"""Reusable RPLIDAR C1 reader module (USB serial).

Usage:
  from lidar_reader import LidarReader

  reader = LidarReader(port="COM4")
  reader.start()
  dist = reader.get_distance_at(90.0)   # mm straight ahead
  obstacles = reader.get_obstacles_in_sector(-30, 30)  # front
  reader.stop()
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ScanPoint:
    """A single LIDAR measurement."""
    angle_deg: float
    distance_mm: float
    quality: int


class LidarReader:
    """Reads RPLIDAR C1 scans in a background thread.

    Stores the latest full 360-degree scan as a dictionary
    keyed by integer angle (0-359).
    """

    def __init__(self, port: str = "COM4", baudrate: int = 115200) -> None:
        self._port = port
        self._baudrate = baudrate
        self._lidar: Optional[object] = None
        self._lock = threading.Lock()
        # Latest scan: angle_deg (int) -> distance_mm (float)
        self._scan_map: Dict[int, float] = {}
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def start(self) -> None:
        """Open the LIDAR and start the polling thread."""
        try:
            from rplidar import RPLidar
        except Exception:
            raise RuntimeError(
                "Failed to import rplidar. Install with: pip install rplidar"
            )

        self._lidar = RPLidar(self._port, baudrate=self._baudrate)
        time.sleep(0.2)

        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the polling thread and disconnect the LIDAR."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        if self._lidar:
            try:
                self._lidar.stop()
            except Exception:
                pass
            try:
                self._lidar.disconnect()
            except Exception:
                pass

    def get_scan_map(self) -> Dict[int, float]:
        """Return a copy of the latest scan map {angle_deg: distance_mm}."""
        with self._lock:
            return dict(self._scan_map)

    def get_distance_at(self, angle: float) -> Optional[float]:
        """Get the distance (mm) at a given angle (degrees, 0-359).

        Returns None if no measurement exists for that angle.
        """
        idx = int(round(angle)) % 360
        with self._lock:
            return self._scan_map.get(idx)

    def get_obstacles_in_sector(
        self,
        start_angle: float,
        end_angle: float,
        max_distance: float = 1000.0,
    ) -> List[Tuple[float, float]]:
        """Return list of (angle, distance_mm) for obstacles within the
        given angular sector that are closer than max_distance (mm).

        Angles wrap around 0/360 correctly.
        """
        start_i = int(round(start_angle)) % 360
        end_i = int(round(end_angle)) % 360
        results: List[Tuple[float, float]] = []

        with self._lock:
            sm = self._scan_map

            if start_i <= end_i:
                angles = range(start_i, end_i + 1)
            else:
                angles = list(range(start_i, 360)) + list(range(0, end_i + 1))

            for a in angles:
                d = sm.get(a)
                if d is not None and d > 0 and d < max_distance:
                    results.append((float(a), d))

        return results

    def get_closest_in_sector(
        self,
        start_angle: float,
        end_angle: float,
    ) -> Optional[Tuple[float, float]]:
        """Find the closest obstacle in the sector.

        Returns (angle, distance_mm) or None.
        """
        pts = self.get_obstacles_in_sector(start_angle, end_angle)
        if not pts:
            return None
        return min(pts, key=lambda p: p[1])

    def _poll_loop(self) -> None:
        """Background loop: read scans and update the map."""
        if self._lidar is None:
            return

        try:
            for scan in self._lidar.iter_scans():
                if not self._running:
                    break

                new_map: Dict[int, float] = {}
                for item in scan:
                    quality, angle_deg, distance_mm = item
                    if distance_mm > 0:
                        idx = int(round(angle_deg)) % 360
                        # Only keep the closest reading at each angle
                        if idx not in new_map or distance_mm < new_map[idx]:
                            new_map[idx] = distance_mm

                with self._lock:
                    self._scan_map = new_map
        except Exception:
            pass


if __name__ == "__main__":
    reader = LidarReader(port="COM4")
    reader.start()
    try:
        for _ in range(20):
            front = reader.get_distance_at(0)
            left = reader.get_distance_at(90)
            right = reader.get_distance_at(270)
            print(f"Front: {front:.0f} mm, Left: {left:.0f} mm, Right: {right:.0f} mm")
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        reader.stop()
        print("LidarReader stopped.")
