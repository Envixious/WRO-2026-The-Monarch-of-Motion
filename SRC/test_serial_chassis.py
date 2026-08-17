import unittest
from unittest.mock import MagicMock, patch

from serial_chassis import SerialChassis


class DummyThread:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        return None

    def join(self, timeout=None):
        return None

    def is_alive(self):
        return False


class SerialChassisTests(unittest.TestCase):
    def test_forward_sends_xy_vector(self) -> None:
        mock_serial = MagicMock()
        with patch("serial_chassis.serial.Serial", return_value=mock_serial), patch("serial_chassis.threading.Thread", DummyThread):
            chassis = SerialChassis(port="/dev/ttyS2")
            chassis.forward(speed=0.5)

        written = b"".join(call.args[0] for call in mock_serial.write.call_args_list)
        self.assertIn(b"0,50\n", written)

    def test_stop_sends_zero_zero(self) -> None:
        mock_serial = MagicMock()
        with patch("serial_chassis.serial.Serial", return_value=mock_serial), patch("serial_chassis.threading.Thread", DummyThread):
            chassis = SerialChassis(port="/dev/ttyS2")
            chassis.stop()

        written = b"".join(call.args[0] for call in mock_serial.write.call_args_list)
        self.assertIn(b"0,0\n", written)


if __name__ == "__main__":
    unittest.main()
