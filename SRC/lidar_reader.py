"""Compatibility wrapper for the shared LiDAR snapshot produced by scan_lidar.py.

The actual scanning and printing are delegated to the dedicated helper scripts,
so this module stays lightweight and only exposes the same simple interface for
existing code paths.

Uses per-call snapshot caching to avoid repeated file I/O.
"""

from __future__ import annotations

import os
import pickle
import time
from typing import Dict, List, Optional, Tuple


class LidarReader:
    """Read the latest LiDAR measurements from the shared pickle file.
    
    Caches snapshots in memory to avoid repeated file I/O on multiple calls.
    """

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        baudrate: int = 460800,
        output_file: Optional[str] = None,
    ) -> None:
        self._port = port
        self._baudrate = baudrate
        self._output_file = output_file or os.environ.get(
            "LIDAR_DATA_PATH",
            "/dev/shm/lidar.data",
        )
        self._last_error: Optional[str] = None
        self._available = False
        self._cached_snapshot: Optional[Dict[int, float]] = None
        self._cache_timestamp = 0.0
        self._cache_ttl = 0.1  # Cache for 100ms (max 1 iteration at 10 Hz)

    def start(self) -> bool:
        """Mark the reader as ready; the real scanning is handled by scan_lidar.py."""
        self._last_error = None
        self._available = True
        return True

    def stop(self) -> None:
        """Stop the compatibility reader."""
        self._available = False
        self._cached_snapshot = None

    def get_output_file_path(self) -> str:
        """Return the shared LiDAR snapshot path."""
        return self._output_file

    def is_available(self) -> bool:
        """Return True when the shared LiDAR snapshot file exists."""
        return self._available and os.path.exists(self._output_file)

    def get_last_error(self) -> str:
        """Return the most recent error message."""
        return self._last_error or ""

    def _load_snapshot(self, use_cache: bool = True) -> Optional[Dict[int, float]]:
        """Load the latest scan snapshot from the shared pickle file.
        
        Args:
            use_cache: If True, reuse cached snapshot if still fresh (default True).
        """
        # Check if we can use cached snapshot (still within TTL)
        if use_cache and self._cached_snapshot is not None:
            age = time.time() - self._cache_timestamp
            if age < self._cache_ttl:
                return self._cached_snapshot  # Use cached, avoid file I/O
        
        # Cache miss or expired: reload from disk
        if not self._output_file or not os.path.exists(self._output_file):
            return None

        try:
            with open(self._output_file, "rb") as handle:
                payload = pickle.load(handle)
            if isinstance(payload, dict):
                self._cached_snapshot = {int(angle): float(distance) for angle, distance in payload.items()}
                self._cache_timestamp = time.time()
                return self._cached_snapshot
        except Exception as exc:
            self._last_error = str(exc)

        return None

    def get_scan_map(self) -> Dict[int, float]:
        """Return a copy of the latest scan map {angle_deg: distance_mm}."""
        snapshot = self._load_snapshot()
        return dict(snapshot or {})

    def get_distance_at(self, angle: float) -> Optional[float]:
        """Get the distance (mm) at a given angle (degrees, 0-359)."""
        snapshot = self._load_snapshot()
        if not snapshot:
            return None
        idx = int(round(angle)) % 360
        return snapshot.get(idx)

    def get_obstacles_in_sector(
        self,
        start_angle: float,
        end_angle: float,
        max_distance: float = 1000.0,
    ) -> List[Tuple[float, float]]:
        """Return the obstacles in a sector based on the shared snapshot."""
        snapshot = self._load_snapshot()
        if not snapshot:
            return []

        start_i = int(round(start_angle)) % 360
        end_i = int(round(end_angle)) % 360
        results: List[Tuple[float, float]] = []

        if start_i <= end_i:
            angles = range(start_i, end_i + 1)
        else:
            angles = list(range(start_i, 360)) + list(range(0, end_i + 1))

        for angle in angles:
            distance = snapshot.get(angle)
            if distance is not None and distance > 0 and distance < max_distance:
                results.append((float(angle), float(distance)))

        return results

    def get_closest_in_sector(
        self,
        start_angle: float,
        end_angle: float,
    ) -> Optional[Tuple[float, float]]:
        """Find the closest obstacle in the sector."""
        pts = self.get_obstacles_in_sector(start_angle, end_angle)
        if not pts:
            return None
        return min(pts, key=lambda p: p[1])
