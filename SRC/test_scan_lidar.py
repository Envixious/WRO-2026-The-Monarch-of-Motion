import unittest
from unittest.mock import Mock

from scan_lidar import cleanup_lidar


class ScanLidarTests(unittest.TestCase):
    def test_cleanup_lidar_calls_reset_and_shutdown(self) -> None:
        lidar = Mock()

        cleanup_lidar(lidar)

        lidar.reset.assert_called_once_with()
        lidar.shutdown.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
