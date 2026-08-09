"""Chassis motor control for a 2WD RWD robot car (Orange Pi 5 / Raspberry Pi).

Hardware assumptions:
  - Single-board computer: Orange Pi 5 (recommended) or Raspberry Pi (2/3/4/5)
  - Motor driver: L298N or similar (uses 2 PWM + 2 direction pins per motor)
  - 2WD with rear-wheel drive (RWD): motors on the rear axle,
    front wheels are free-rolling casters.
  - Differential steering:
      * Forward:  both motors spin forward
      * Backward:  both motors spin reverse
      * Turn left: right motor forward, left wheel stopped
      * Turn right: left motor forward, right wheel stopped

Orange Pi 5 note:
  - Orange Pi 5 uses the OPi.GPIO library (API-compatible with RPi.GPIO).
  - Install: pip install OPi.GPIO
  - BCM pin numbering is used below (same numbering as Raspberry Pi).

Wiring (adjust to your actual GPIO pins - BCM numbering):
  Motor A (left rear)
    IN1 -> GPIO17 (Physical pin 11)
    IN2 -> GPIO18 (Physical pin 12)
    ENA -> GPIO12 (Physical pin 32) - PWM0

  Motor B (right rear)
    IN3 -> GPIO22 (Physical pin 15)
    IN4 -> GPIO23 (Physical pin 16)
    ENB -> GPIO13 (Physical pin 33) - PWM1

Usage:
  from chassis_control import Chassis

  car = Chassis()
  car.forward(speed=0.6)
  time.sleep(2)
  car.turn_left(speed=0.4)
  time.sleep(1)
  car.stop()
"""

from __future__ import annotations

import importlib
import time

# --- Board-agnostic GPIO import ---
# Try OPi.GPIO first (Orange Pi), fall back to RPi.GPIO (Raspberry Pi)
GPIO = None

for _mod_name in ("OPi.GPIO", "RPi.GPIO"):
    try:
        GPIO = importlib.import_module(_mod_name)
        break
    except (ImportError, ModuleNotFoundError):
        continue

if GPIO is None:
    raise RuntimeError(
        "No GPIO library found.\n"
        "  Orange Pi 5:  pip install OPi.GPIO\n"
        "  Raspberry Pi: pip install RPi.GPIO"
    )
# ----------------------------------

# ---------- Default GPIO pin assignments (BCM numbering) ----------
PIN_A_IN1 = 17
PIN_A_IN2 = 18
PIN_A_ENA = 12

PIN_B_IN3 = 22
PIN_B_IN4 = 23
PIN_B_ENB = 13

PWM_FREQ = 100  # Hz
# -----------------------------------------------------------------


class Chassis:
    """2WD differential-drive chassis controller (RWD)."""

    def __init__(
        self,
        in1: int = PIN_A_IN1,
        in2: int = PIN_A_IN2,
        ena: int = PIN_A_ENA,
        in3: int = PIN_B_IN3,
        in4: int = PIN_B_IN4,
        enb: int = PIN_B_ENB,
        pwm_freq: int = PWM_FREQ,
    ) -> None:
        GPIO.setmode(GPIO.BCM)

        for pin in (in1, in2, in3, in4):
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        for pin in (ena, enb):
            GPIO.setup(pin, GPIO.OUT)

        self._pwm_a = GPIO.PWM(ena, pwm_freq)
        self._pwm_b = GPIO.PWM(enb, pwm_freq)
        self._pwm_a.start(0)
        self._pwm_b.start(0)

        self._in1 = in1
        self._in2 = in2
        self._in3 = in3
        self._in4 = in4

    def _set_motor(self, motor: int, forward: bool, speed: float) -> None:
        """Set a single motor.

        Args:
            motor: 0 = left, 1 = right
            forward: True=forward, False=reverse
            speed:  0.0 to 1.0
        """
        if motor == 0:
            in_a, in_b = self._in1, self._in2
            pwm = self._pwm_a
        else:
            in_a, in_b = self._in3, self._in4
            pwm = self._pwm_b

        speed = max(0.0, min(1.0, speed))
        duty = speed * 100.0

        if forward:
            GPIO.output(in_a, GPIO.HIGH)
            GPIO.output(in_b, GPIO.LOW)
        else:
            GPIO.output(in_a, GPIO.LOW)
            GPIO.output(in_b, GPIO.HIGH)

        pwm.ChangeDutyCycle(duty)

    def forward(self, speed: float = 0.5) -> None:
        self._set_motor(0, forward=True, speed=speed)
        self._set_motor(1, forward=True, speed=speed)

    def backward(self, speed: float = 0.5) -> None:
        self._set_motor(0, forward=False, speed=speed)
        self._set_motor(1, forward=False, speed=speed)

    def turn_left(self, speed: float = 0.3) -> None:
        """Pivot left (right wheel forward, left stopped)."""
        self._set_motor(0, forward=True, speed=0.0)
        self._set_motor(1, forward=True, speed=speed)

    def turn_right(self, speed: float = 0.3) -> None:
        """Pivot right (left wheel forward, right stopped)."""
        self._set_motor(0, forward=True, speed=speed)
        self._set_motor(1, forward=True, speed=0.0)

    def spin_left(self, speed: float = 0.3) -> None:
        """Spin in place left (tank turn)."""
        self._set_motor(0, forward=False, speed=speed)
        self._set_motor(1, forward=True, speed=speed)

    def spin_right(self, speed: float = 0.3) -> None:
        """Spin in place right (tank turn)."""
        self._set_motor(0, forward=True, speed=speed)
        self._set_motor(1, forward=False, speed=speed)

    def stop(self) -> None:
        self._set_motor(0, forward=True, speed=0.0)
        self._set_motor(1, forward=True, speed=0.0)

    def cleanup(self) -> None:
        try:
            self.stop()
            self._pwm_a.stop()
            self._pwm_b.stop()
        except Exception:
            pass
        GPIO.cleanup()

    def __enter__(self) -> Chassis:
        return self

    def __exit__(self, *args) -> None:
        self.cleanup()


# ---- Interactive test (run directly) ----
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test chassis motors")
    parser.add_argument("--speed", type=float, default=0.4, help="Speed 0.0-1.0")
    args = parser.parse_args()

    print("Chassis test - Ctrl+C to stop early")
    with Chassis() as car:
        try:
            print("Forward 2s")
            car.forward(speed=args.speed)
            time.sleep(2)

            print("Stop 1s")
            car.stop()
            time.sleep(1)

            print("Backward 2s")
            car.backward(speed=args.speed)
            time.sleep(2)

            print("Stop 1s")
            car.stop()
            time.sleep(1)

            print("Turn left 1.5s")
            car.turn_left(speed=args.speed)
            time.sleep(1.5)

            print("Turn right 1.5s")
            car.turn_right(speed=args.speed)
            time.sleep(1.5)

            print("Spin left 1.5s")
            car.spin_left(speed=args.speed)
            time.sleep(1.5)

            print("Spin right 1.5s")
            car.spin_right(speed=args.speed)
            time.sleep(1.5)

        except KeyboardInterrupt:
            pass

        print("Stopped")
