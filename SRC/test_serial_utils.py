import unittest
from unittest.mock import patch

from serial_utils import resolve_serial_port


class ResolveSerialPortTests(unittest.TestCase):
    def test_auto_prefers_provided_candidates_when_available(self) -> None:
        with patch("serial_utils.get_available_ports", return_value=["COM3", "/DEV/TTYUSB0"]):
            self.assertEqual(resolve_serial_port("auto", candidates=["/DEV/TTYUSB0", "COM3"]), "/DEV/TTYUSB0")

    def test_explicit_requested_port_is_used_when_present(self) -> None:
        with patch("serial_utils.get_available_ports", return_value=["/DEV/TTYUSB0"]):
            self.assertEqual(resolve_serial_port("/DEV/TTYUSB0"), "/DEV/TTYUSB0")

    def test_missing_port_raises_helpful_error(self) -> None:
        with patch("serial_utils.get_available_ports", return_value=[]):
            with self.assertRaises(RuntimeError):
                resolve_serial_port("auto", candidates=["/DEV/TTYUSB0"])


if __name__ == "__main__":
    unittest.main()
