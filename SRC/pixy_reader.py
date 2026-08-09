"""Reusable PixyCam2 reader module (USB).

Signature mapping (trained by user):
  sig1 = green
  sig2 = red
  sig3 = pink
  sig4 = orange
  sig5 = blue

Usage:
  from pixy_reader import PixyReader

  reader = PixyReader()
  reader.start()
  colors = reader.get_detected_colors()
  # [("green", x_position), ("pink", 150), ...]
  reader.stop()
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import List, Optional


# Mapping Pixy2 signature numbers to color names
# sig1=green, sig2=red, sig3=pink, sig4=orange, sig5=blue
SIGNATURE_MAP = {
    1: "green",
    2: "red",
    3: "pink",
    4: "orange",
    5: "blue",
}


@dataclass
class ColorDetection:
    """A single color blob detected by PixyCam2."""
    color: str
    x: int            # centre x position (0-319)
    y: int            # centre y position (0-199)
    width: int        # bounding box width
    height: int       # bounding box height
    signature: int    # raw signature number


class PixyReader:
    """Reads PixyCam2 blocks in a background thread.

    Call start() to begin polling, then get_detected_colors()
    to retrieve the latest frame of detections.
    """

    def __init__(self) -> None:
        self._cam: Optional[object] = None
        self._lock = threading.Lock()
        self._detections: List[ColorDetection] = []
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def start(self) -> None:
        """Initialise the camera and start the polling thread."""
        try:
            import pixy2  # type: ignore
        except Exception:
            raise RuntimeError(
                "Failed to import pixy2 module. Install the Pixy2 Python wrapper."
            )

        self._cam = pixy2.Pixy2()
        try:
            self._cam.init()
        except AttributeError:
            pass  # some wrappers auto-init

        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the polling thread and release the camera."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        if self._cam:
            for method_name in ("close", "stop"):
                try:
                    getattr(self._cam, method_name)()
                except Exception:
                    pass

    def get_detected_colors(self) -> List[ColorDetection]:
        """Return the latest frame of colour detections."""
        with self._lock:
            return list(self._detections)

    def get_latest_colors(self) -> List[str]:
        """Convenience: return just the colour names detected."""
        return [d.color for d in self.get_detected_colors()]

    def _poll_loop(self) -> None:
        """Background loop: poll Pixy2 blocks at ~20 Hz."""
        while self._running:
            try:
                if self._cam is None:
                    continue
                blocks = self._cam.get_blocks()
            except Exception:
                blocks = None

            parsed: List[ColorDetection] = []
            if blocks:
                for b in blocks:
                    sig = getattr(b, "signature", None) if not isinstance(b, dict) else b.get("signature")
                    x = getattr(b, "x", None) if not isinstance(b, dict) else b.get("x")
                    y = getattr(b, "y", None) if not isinstance(b, dict) else b.get("y")
                    w = getattr(b, "width", None) if not isinstance(b, dict) else b.get("width")
                    h = getattr(b, "height", None) if not isinstance(b, dict) else b.get("height")

                    color = SIGNATURE_MAP.get(sig, f"sig{sig}")
                    if color and x is not None:
                        parsed.append(ColorDetection(
                            color=color,
                            x=int(x), y=int(y or 0),
                            width=int(w or 0), height=int(h or 0),
                            signature=int(sig or 0),
                        ))

            with self._lock:
                self._detections = parsed

            time.sleep(0.05)  # ~20 Hz


if __name__ == "__main__":
    # Quick test
    reader = PixyReader()
    reader.start()
    try:
        for _ in range(50):
            detections = reader.get_detected_colors()
            colors = [d.color for d in detections]
            print(f"Detected: {colors}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        reader.stop()
        print("PixyReader stopped.")
