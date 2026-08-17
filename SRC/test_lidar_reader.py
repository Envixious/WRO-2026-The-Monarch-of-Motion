import tempfile
import unittest
from pathlib import Path

from lidar_reader import LidarReader


class LidarReaderTests(unittest.TestCase):
    def test_start_marks_reader_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            snapshot_path = Path(tmp_dir) / "lidar.data"
            snapshot_path.write_bytes(b"{}")

            reader = LidarReader(port="/dev/ttyUSB0", output_file=str(snapshot_path))
            self.assertTrue(reader.start())
            self.assertTrue(reader.is_available())


if __name__ == "__main__":
    unittest.main()
