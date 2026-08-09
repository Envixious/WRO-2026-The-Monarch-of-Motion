# RPLIDAR C1 -> Self-driving robot basic steps

- [x] Create basic Python script to read USB serial scans from RPLIDAR C1
- [x] Create basic PixyCam2 USB reader scaffold (pixycam2_basic.py)
- [x] Create chassis motor control module (chassis_control.py) for 2WD RWD car
- [x] Update chassis_control.py to support Orange Pi 5 (OPi.GPIO) & Raspberry Pi (RPi.GPIO)
- [x] Create reusable PixyCam2 reader module (pixy_reader.py) with background thread
- [x] Create reusable RPLIDAR reader module (lidar_reader.py) with background thread
- [x] Create parallel parking routine (parallel_park.py) using LiDAR
- [x] Create main fusion decision engine (fusion_main.py) combining all subsystems
- [ ] Add live visualization (matplotlib) of points (optional)
- [ ] Convert polar (angle, distance) to Cartesian (x, y)
- [ ] Build simple occupancy grid
- [ ] Integrate with a SLAM solution (Python or ROS) as next stage
- [ ] Tune parallel park timing/parameters for real-world testing
- [ ] Tune colour-action durations for actual robot response
