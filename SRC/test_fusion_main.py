import pickle
import tempfile
import unittest
from pathlib import Path

from fusion_main import _load_lidar_snapshot


class FusionMainTests(unittest.TestCase):
    def test_load_lidar_snapshot_reads_pickle_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            snapshot_path = Path(tmp_dir) / "lidar.data"
            with snapshot_path.open("wb") as handle:
                pickle.dump({0: 100, 90: 200}, handle)

            self.assertEqual(_load_lidar_snapshot(str(snapshot_path)), {0: 100, 90: 200})

    def test_load_lidar_snapshot_returns_none_for_missing_file(self) -> None:
        self.assertIsNone(_load_lidar_snapshot("/tmp/does-not-exist-12345"))


if __name__ == "__main__":
    unittest.main()
