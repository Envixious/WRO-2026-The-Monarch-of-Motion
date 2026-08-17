"""Utilities for resolving serial ports in a friendly way."""

from __future__ import annotations

import sys
from typing import Iterable, List, Optional

try:
    import serial.tools.list_ports as list_ports
except Exception:  # pragma: no cover - platform may not expose pyserial fully
    list_ports = None


def get_available_ports() -> List[str]:
    """Return a list of currently available serial ports."""
    if list_ports is None:
        return []
    try:
        ports = list_ports.comports()
    except Exception:
        return []

    return [port.device for port in ports if getattr(port, "device", None)]


def resolve_serial_port(port: Optional[str], candidates: Optional[Iterable[str]] = None) -> str:
    """Resolve a serial port, preferring an explicit value or a discovered one.

    If ``port`` is None or ``auto``, this will try the provided candidates in order
    and otherwise use the first available port discovered by pyserial.
    """
    if port and str(port).strip().lower() not in {"", "auto", "none"}:
        return str(port)

    preferred = [str(c) for c in (candidates or []) if str(c).strip()]
    if preferred:
        available = get_available_ports()
        for candidate in preferred:
            if candidate in available:
                return candidate

    available = get_available_ports()
    if available:
        return available[0]

    raise RuntimeError(
        "No serial ports were detected. Connect the device and retry, or pass --port with a valid COM/ttyUSB value."
    )


def print_port_help() -> None:
    """Print a helpful diagnostic for the user."""
    available = get_available_ports()
    if available:
        print("Detected serial ports:", ", ".join(available), file=sys.stderr)
    else:
        print("No serial ports detected.", file=sys.stderr)
