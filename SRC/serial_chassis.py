"""Serial-based chassis adapter for an ESP32 servo bridge.

The Orange Pi sends movement commands as a simple ``x,y`` string over serial,
where both x and y are integers from -100 to 100:
  - x: steering angle (0=straight, 1-100=right, -1 to -100=left)
  - y: throttle (-100=full reverse, 0=stop, 100=full forward)

Value-to-Physical Mapping:
  - Steering: 1 unit = 0.5°
    * 0     → 0° (straight)
    * 100   → 50° (max right)
    * -100  → -50° (max left)
    * 50    → 25° (half right)
    * -30   → -15° (half left)
  
  - Throttle: 1 unit = 1% speed
    * 0     → 0% (stopped)
    * 100   → 100% (full forward)
    * -50   → 50% reverse
    * 30    → 30% forward

Example commands:
  "0,50\n"    -> 50% forward, straight wheels
  "30,0\n"    -> 15° right steering, stopped
  "-50,75\n"  -> 25° left + 75% forward throttle
  "100,100\n" -> 50° right + 100% forward
  "0,0\n"     -> Full stop, straight wheels

The ESP32 firmware is expected to parse the line and translate it into servo commands.
"""

from __future__ import annotations

import threading
import time
from typing import Optional

import serial


class SerialChassis:
    def __init__(self, port: str, baud: int = 115200, timeout: float = 0.1) -> None:
        try:
            self._ser = serial.Serial(port, baud, timeout=timeout)
        except Exception as exc:
            raise RuntimeError(f"Cannot open serial port {port}: {exc}") from exc
        self._lock = threading.Lock()
        self._running = True
        self._last_error_time = 0.0
        
        # State tracking: only send commands when state changes
        self._last_x = None
        self._last_y = None
        self._commands_sent = 0
        self._commands_skipped = 0

    def _send_vector(self, x: int, y: int) -> None:
        """Send movement command only if state changed. Skip duplicate commands.
        
        Args:
            x: Steering value from -100 (50° left) to 100 (50° right), 0 is straight.
               Each unit = 0.5°. Range: -100 to 100.
            y: Throttle value from -100 (full reverse) to 100 (full forward), 0 is stop.
               Range: -100 to 100.
        """
        # Clamp values to valid range
        x = max(-100, min(100, x))
        y = max(-100, min(100, y))
        
        # Only send if this is a new command (state changed)
        if x == self._last_x and y == self._last_y:
            self._commands_skipped += 1
            return  # No state change; don't send
        
        # State changed: update and send 
        self._last_x = x
        self._last_y = y
        self._commands_sent += 1
        
        line = f"{x},{y}\n".encode("ascii")
        with self._lock:
            try:
                self._ser.write(line)
                self._ser.flush()  # Ensure command is sent immediately
            except Exception as exc:
                print(f"[chassis] WARNING: Failed to send vector ({x},{y}): {exc}")

    def forward(self, speed: int = 50) -> None:
        """Move forward at specified speed (1-100, where 100 is max speed)."""
        speed = max(1, min(100, speed))  # Clamp to 1-100
        self._send_vector(0, speed)

    def backward(self, speed: int = 50) -> None:
        """Move backward at specified speed (1-100, where 100 is max speed)."""
        speed = max(1, min(100, speed))  # Clamp to 1-100
        self._send_vector(0, -speed)

    def turn_left(self, angle: int = 30, speed: int = 30) -> None:
        """Turn left while moving forward at specified angle and speed.
        
        Args:
            angle: Steering value 1-100. Each unit = 0.5°.
                   30 = 15° left, 100 = 50° left (max). Default 30.
            speed: Forward throttle during turn (1-100). Default 30.
                   Replicates real car behavior of steering + forward motion.
        """
        angle = max(1, min(100, angle))  # Clamp to 1-100
        speed = max(1, min(100, speed))  # Clamp to 1-100
        self._send_vector(-angle, speed)  # Steering + forward throttle

    def turn_right(self, angle: int = 30, speed: int = 30) -> None:
        """Turn right while moving forward at specified angle and speed.
        
        Args:
            angle: Steering value 1-100. Each unit = 0.5°.
                   30 = 15° right, 100 = 50° right (max). Default 30.
            speed: Forward throttle during turn (1-100). Default 30.
                   Replicates real car behavior of steering + forward motion.
        """
        angle = max(1, min(100, angle))  # Clamp to 1-100
        speed = max(1, min(100, speed))  # Clamp to 1-100
        self._send_vector(angle, speed)  # Steering + forward throttle

    def spin_left(self, speed: int = 50) -> None:
        """Spin left in place using full steering lock (50° left).
        
        Args:
            speed: Forward throttle during spin (1-100, default 50).
                   Uses maximum steering angle for rotation.
                   30 = gentle spin, 100 = aggressive spin.
        """
        speed = max(1, min(100, speed))  # Clamp to 1-100
        self._send_vector(-100, speed)  # Full left steering + forward throttle

    def spin_right(self, speed: int = 50) -> None:
        """Spin right in place using full steering lock (50° right).
        
        Args:
            speed: Forward throttle during spin (1-100, default 50).
                   Uses maximum steering angle for rotation.
                   30 = gentle spin, 100 = aggressive spin.
        """
        speed = max(1, min(100, speed))  # Clamp to 1-100
        self._send_vector(100, speed)  # Full right steering + forward throttle

    def stop(self) -> None:
        self._send_vector(0, 0)

    def get_stats(self) -> dict:
        """Return serial communication statistics."""
        return {
            "commands_sent": self._commands_sent,
            "commands_skipped": self._commands_skipped,
            "last_state": (self._last_x, self._last_y),
        }

    def cleanup(self) -> None:
        try:
            self.stop()
        except Exception:
            pass
        self._running = False
        try:
            self._ser.close()
        except Exception:
            pass

    def __enter__(self) -> "SerialChassis":
        return self

    def __exit__(self, *args) -> None:
        self.cleanup()
