# RPLIDAR C1 basic USB serial reader (Python)

This folder contains a minimal script to read and print scan points from the **SLAMTEC RPLIDAR C1**.

## 1) Install dependency
```bash
pip install rplidar
```

## 2) Set the correct COM port
Edit `basic_rplidar_c1.py` or pass it as a flag.

On Windows it usually looks like `COM3`, `COM4`, etc.

## 3) Run
```bash
python basic_rplidar_c1.py --port COM4
```

You should see lines like:
- `angle=... deg, distance=... mm`

## Notes
- This is the “raw data” starting point. Next steps typically add:
  - filtering / clustering
  - converting to Cartesian coordinates
  - feeding points into SLAM (e.g., `gmapping`, `hector_slam`, or a Python SLAM stack)

