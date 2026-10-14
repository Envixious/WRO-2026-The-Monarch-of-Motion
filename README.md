# WRO 2026 Future Engineers — [The Monarch of Motion]
## 1. Project overview

**Team:** [The Monarch of Motion]  
**Country:** Indonesia  
**Competition:** WRO 2026 Future Engineers  
**Robot name:** [The Monarch of Motion] 
**Team members:** [Evan Felix Santoso], [Caitlyn Calina Lievee]  
**Coach:** [Mr. Nikhil Loyola Dzousa]

[## Autonomous Vehicle Overview

**The Monarch of Motion (MOM)** is an autonomous vehicle developed for the WRO Future Engineers competition. The vehicle is designed to navigate the competition field, detect track boundaries and obstacles, determine its driving direction, complete the required laps, and perform autonomous parking without human control.

MOM has compact dimensions of 290 mm in length, 150 mm in width, and 135 mm in height. These dimensions remain within the WRO maximum vehicle size of 300 mm × 200 mm × 300 mm. Its low-profile design helps lower the centre of gravity, improving stability during cornering and reducing unnecessary body movement.


The vehicle uses a rear-wheel-drive system powered by one **JGA25-370 DC** geared motor. This configuration complies with the WRO rule allowing a maximum of one drive motor. Rear-wheel drive provides a simple and efficient mechanical arrangement while leaving the front section available for the steering mechanism and sensors.

Steering is controlled by one **MG996 servo motor** connected to an **Ackermann steering system**. This also complies with the WRO rule permitting a maximum of one steering motor. Ackermann steering allows the inner and outer front wheels to turn at different angles during a corner, reducing tyre slip and improving turning accuracy.

The main processing system consists of an **Orange Pi 5 Pro** and an **ESP32**. The Orange Pi 5 Pro functions as the vehicle’s main computer or “brain.” It is responsible for high-level tasks such as sensor processing, obstacle detection, navigation decisions, route planning, and competition strategy. The ESP32 functions as the real-time control unit. It receives instructions from the Orange Pi 5 Pro and controls the drive motor, steering servo, and other low-level hardware functions.

The software is developed using **Visual Studio Code** with **Python** as the main programming language. Python is used because it supports rapid development, sensor integration, computer vision, data processing, and clear modular programming. The ESP32 may use separate firmware for direct motor and servo control, while communication between the Orange Pi 5 Pro and ESP32 allows the system to separate high-level decision-making from time-sensitive hardware control.

For visual detection, MOM uses a **PixyCam2**. The camera is intended to identify important visual features such as coloured obstacles, track elements, and navigation markers. Because PixyCam2 performs some image processing internally, it can reduce the processing workload placed on the Orange Pi 5 Pro.

A **SLAMTEC RPLIDAR C1** provides distance measurements around the vehicle. The LiDAR can be used to detect walls, estimate the vehicle’s position relative to track boundaries, measure available space, and support obstacle avoidance. Its wide scanning range gives the vehicle more environmental information than a small number of fixed distance sensors.

MOM uses a **Single-battery system**. The battery that is used Black Cell 1500 mAH 60 C high Drain LiPO 11 V. According to the theory, the battery can supply the computing system and the motor system separately, although the robot needs to separate regulated branches for the computing system and the motor/servo system. This arrangement also reduces the risk of electrical noise or sudden demand from the drive motor and steering servo will cause voltage drops, interfere with the sensors, or restart the Orange Pi 5 Pro. This design also keeps the size of the robot light, makes the wiring less complicated, gives more space, and minimizes the possibility of potential electrical failure.

## Main Strengths

One of the main strengths of MOM is its **hybrid control architecture**. The Orange Pi 5 Pro handles complex navigation and sensor-processing tasks, while the ESP32 manages direct hardware control. This division reduces the workload on each controller and allows the motor and steering system to respond quickly even when the Orange Pi 5 Pro is processing camera or LiDAR data.

The combination of the **PixyCam2 and RPLIDAR C1** gives the robot two different types of environmental information. The camera can classify coloured objects, while the LiDAR can measure distance and detect surrounding structures. Using both sensors may improve reliability because the robot is not dependent on only one sensing method.

The vehicle’s **compact and low-profile chassis** is another advantage. Its dimensions provide sufficient space for the electronics while remaining comfortably inside the WRO size limits. The low height may improve stability and reduce the risk of excessive body movement during fast turns.

The **Ackermann steering mechanism** provides more realistic and controlled cornering than a simple parallel steering linkage. It can reduce wheel scrubbing, improve turning consistency, and allow better control of the vehicle’s path around corners.

The **rear-wheel-drive layout** is mechanically simple and allows the front wheels to focus only on steering. This separation may make the vehicle easier to maintain, calibrate, and troubleshoot.

The single-battery architecture was selected to reduce weight, wiring complexity, space requirements, and the number of potential electrical failure points. Although the robot uses a common energy source, the computing, sensor, steering, and drive systems are supplied through separate regulated power branches. This provides the practical simplicity of a single battery while reducing the risk of voltage fluctuations from the motor system affecting the Orange Pi 5 Pro and sensors

## Current Limitations

The most significant limitation is the **complexity of integrating several controllers and sensors**. The Orange Pi 5 Pro, ESP32, PixyCam2, RPLIDAR C1, motor driver, and servo must communicate reliably. Communication delays, incorrect data formats, disconnected cables, or software crashes could affect the entire vehicle.

The **Orange Pi 5 Pro has relatively high power consumption** compared with a small microcontroller. It may also produce heat during continuous image processing and LiDAR data processing. The vehicle therefore requires effective voltage regulation, cooling, cable management, and power monitoring.

The **PixyCam2 may be affected by lighting conditions, reflections, shadows, and colours similar to the competition obstacles**. Its performance will depend on careful colour calibration and repeated testing under different lighting environments.

The **RPLIDAR C1 adds weight and requires a clear scanning area**. Its measurements may also be affected by vibration, reflective surfaces, incorrect mounting, or temporary obstruction by parts of the robot. Processing a large amount of LiDAR data may increase the load on the Orange Pi 5 Pro.

The **MG996 servo can draw a high current**, especially when the steering mechanism is under load. It may also have mechanical backlash, which can reduce steering precision. The steering linkage must therefore be rigid, correctly aligned, and carefully calibrated.

Using only one JGA25-370 drive motor creates a **single point of failure**. If the motor, gearbox, wheel connection, or motor driver fails, the vehicle cannot move. Rear-wheel drive may also experience reduced traction during rapid acceleration, sharp turning, or movement on a dusty competition surface.

Finally, the chassis height of only 55 mm creates **limited internal space**. Components must be arranged carefully to prevent cable interference, overheating, blocked LiDAR scans, restricted airflow, or contact between moving steering parts and electronic components.

Overall, MOM has a strong foundation because it combines a compact mechanical platform, Ackermann steering, rear-wheel drive, high-level computing, real-time motor control, camera detection, and LiDAR sensing. Its final performance will depend on careful integration, power management, calibration, repeated testing, and simplification of any system that does not provide a clear improvement in reliability.]


## 2. Repository contents

- `docs/` — engineering journal, build guide, bill of materials, decisions, risks, testing, and releases.
- `t-photos/` — team photographs.
- `v-photos/` — vehicle photographs from front, rear, left, right, top, and bottom.
- `video/` — YouTube links for autonomous demonstrations of both challenges.
- `schemes/` — wiring, power, electronic, and system architecture diagrams.
- `src/` — complete source code for every programmed controller.
- `other/` — datasets, datasheets, setup notes, and other reproducibility materials.

## 3. Mobility and mechanical design

### 3.1 Chassis

The Monarch of Motion (MOM) uses a compact chassis designed specifically for the WRO Future Engineers competition. The current vehicle dimensions are approximately 290 mm x 150 mm x 135 mm. These dimensions remain within the WRO maximum vehicle dimensions of 300 mm × 200 mm × 300 mm.

The relatively low vehicle height helps maintain a low centre of mass, which improves stability during cornering and reduces unnecessary body movement when the vehicle changes direction. The compact chassis also provides sufficient space for the drive system, steering mechanism, Orange Pi 5 Pro, ESP32, PixyCam2, RPLIDAR C1, batteries, and other electronic components.

The vehicle uses a rear-wheel-drive layout with the steering mechanism located at the front. The front section contains the Ackermann steering system and provides mounting positions for navigation sensors. The Orange Pi 5 Pro, ESP32, batteries, and power electronics are positioned within the main chassis area to keep the vehicle balanced.

The exact chassis material, total vehicle weight, wheelbase, track width, and measured centre-of-mass position are still being finalized and will be recorded after the final mechanical design is completed.

Current chassis specifications:

| Specification | Value |
|---|---:|
| Length | 290 mm |
| Width | 150 mm |
| Height | 135 mm |
| Max WRO Length | 300 mm |
| Max WRO Width | 200 mm |
| Max WRO Height | 300 mm |
| Vehicle Weight | 937 g |
| Wheelbase | 140 mm |
| Front Track Width | 120 mm |
| Rear Track Width | 120 mm |
| Chassis Material | Metal |
| Centre of Mass | Area Containing Battery |

The mounting system is designed to keep the major components securely attached while maintaining enough rigidity to prevent unwanted chassis flex. Particular attention is given to the steering mechanism and sensor mounts because movement or vibration in these areas could reduce navigation accuracy.

### 3.2 Drive mechanism

MOM uses a rear-wheel-drive system powered by one JGA25-370 DC geared motor. The use of one drive motor complies with the WRO Future Engineers requirement allowing a maximum of one motor for propulsion.

The motor is installed at the rear section of the vehicle and transfers power to the rear drive system. Rear-wheel drive was selected because it provides a relatively simple mechanical arrangement and allows the front wheels to be used entirely for steering.

Separating propulsion and steering also simplifies control. The drive motor is responsible for forward and reverse movement, while the front Ackermann steering system controls the vehicle's direction.

The JGA25-370 was selected because geared DC motors of this type provide a useful balance between torque, speed, compact size, and controllability for a small autonomous vehicle.

The final motor driver, gearbox ratio, wheel diameter, encoder specification, and exact transmission arrangement will be documented after the drive system is fully finalized and tested.

Current drive-system specifications:

| Specification | Current Design |
|---|---|
| Drive Layout | Rear-wheel drive |
| Drive Motor | 1 × JGA25-370 DC geared motor |
| Number of Drive Motors | 1 |
| Gear Ratio | 1.35:1 |
| Wheel Diameter | 65 mm |
| Motor Driver | 1 × TB6612FNG Wemos Motor Shield |
| Controller | 1 × ESP32 |
| High-Level Controller | 1 × Orange Pi 5 Pro |

The ESP32 will provide the low-level motor-control commands, while the Orange Pi 5 Pro will determine the required vehicle movement based on information from the navigation sensors.

This configuration was preferred over a more complicated drivetrain because MOM requires reliable and repeatable movement rather than maximum vehicle speed.

### 3.3 Steering mechanism

MOM uses an Ackermann steering system operated by one MG996 servo motor. The use of a single steering servo complies with the WRO requirement permitting a maximum of one motor for steering.

Ackermann steering allows the inner and outer front wheels to turn through different angles while cornering. The inner wheel follows a smaller turning radius than the outer wheel. This reduces tyre scrubbing and allows the vehicle to follow a smoother path through corners.

The MG996 servo controls the steering linkage mechanically connected to the front wheels. The servo receives steering commands from the ESP32, while the steering target is determined by the Orange Pi 5 Pro navigation system.

The steering system will be calibrated around three important reference positions:

centre or straight-ahead position;
maximum safe left steering position;
maximum safe right steering position.

Software limits will be used to prevent the servo from attempting to move beyond the safe mechanical steering range. Mechanical limits will also be considered to prevent excessive movement of the linkage or contact between steering components and the chassis.

The exact steering-angle range will be measured after the final steering linkage is assembled.

Current steering specifications:

| Specification | Current Design |
|---|---|
| Steering Geometry | Ackermann |
| Steering Motor | 1 × MG996 servo |
| Steering Controller | ESP32 |
| Centre Position | 90° |
| Maximum Left Angle | 50° |
| Maximum Right Angle | 130° |
| Software Steering Limits | Left: 50°–90°; Right: 90°–130° |

Ackermann steering was selected because the WRO track contains repeated corners and requires accurate vehicle positioning. Reduced wheel slip should provide better consistency when MOM navigates both the Open Challenge and Obstacle Challenge.

### 3.4 Torque and speed reasoning

To strike a balance between straight-line speed and torque in low-speeds for obstacle navigation and turning, we selected the JGA25-370 DC geared motor. Configured in a rear-wheel-drive layout, it has a 1.35:1 gear ratio driving our 65 mm diameter wheels.

When evaluating our drivetrain options, we analyzed the distinct performance trade-offs associated with different gear ratios. Motors with higher gear ratios and low RPM outputs would have severely limited our top speed during the open challenge laps, this results in uncompetitive times on straightaways, even if we do excel in acceleration out of cornering and avoiding obstacles. On the other hand, utilizing a configuration with lower gear ratios would increase our straight line speed, but we lose important torque necessary for the car to accelerate out of corners or from rest. In practice, we risk the motor stalling during rapid directional changes, dead stops, or the fine-adjustment phase of parallel parking.

MOM’s chosen setup, managed by the TB6612FNG Wemos Motor Shield, an ESP32 microcontroller, and an Orange Pi 5 Pro high-level processor, delivers what we find to be our ideal compromise. The motor provides reliable torque to overcome the static friction of the playmat and weight distribution smoothly, while keeping top speed within a competitive and stable range. The controlled speed also benefits the software, as it prevents motion blur in our PixyCam and ensures our program has ample time to turn before an obstacle or a track barrier.

### 3.5 Mechanical iterations
Mechanical Iterations can be found in Docs/engineering-decisions.md

## 4. Power and sensor architecture

### 4.1 Power system
MOM needs a reliable, stable, and high-performance power supply for its onboard microcontrollers, high-level computer, sensors, and drive actuators. As a result, we chose to equip it with a 1500mAh 3S 130C Lithium Polymer (LiPo) battery. Selecting a 3-cell configuration provides a voltage of 11.1V, however this goes up to 12.6V when fully charged. This voltage level is ideal for directly supplying our motor shield and drive motor, while offering a clean, efficient higher-voltage source that can be stepped down safely to power our logic components.

The 1500mAh capacity balances the power needed for operational runtime and physical weight. There is sufficient capacity to last for multiple testing or competition runs without needing constant recharging while keeping the vehicle's center of gravity and mass low. The battery's high 130C discharge rating also ensures an extremely low internal resistance and a large current headroom. In this category, aggressive accelerations from a dead stop, rapid direction reversals, and sudden motor load spikes can cause severe voltage dips on standard batteries. The 130C rating means that current delivery will remain instantaneous and rock-solid. This protects our sensitive microcontrollers such as our ESP32 and Orange Pi 5 Pro from brownouts or sudden reboots.


### 4.2 Power budget
| Component | Operating Voltage | Typical Operating Current | Maximum / Peak Current | Power Source |
| :--- | :--- | :--- | :--- | :--- |
| **Orange Pi 5 Pro** | 5 V DC | ~1.0 A – 2.5 A (5 W – 12 W) | ~4.0 A (under max stress) | Buck Converter (5 V / 5 A) |
| **ESP32 (Dev Board)** | 5 V (VIN pin) / 3.3 V (internal) | ~80 mA – 150 mA | ~350 mA – 500 mA (RF bursts) | Buck Converter (5 V) |
| **MG996R Servo** | 4.8 V – 7.2 V (6 V recommended) | ~500 mA – 900 mA | ~2.5 A (Stall Current @ 6V) | Buck Converter (6 V / 3 A) |
| **JGA25-370 Motor** | 6 V – 12 V DC (12 V nominal) | ~50 mA – 150 mA (no load) | ~1.2 A – 2.0 A (Stall Current) | Motor Driver fed by Buck Converter / Battery |
| **PixyCam2** | 5 V DC | ~140 mA | ~300 mA – 400 mA (LED on) | Orange Pi 5 Pro USB (5 V) |
| **RPLIDAR C1** | 5 V DC | ~230 mA (operating) | ~260 mA (operating) / ~800 mA (startup pulse) | Orange Pi 5 Pro USB (5 V) |


### 4.3 Sensors and placement

MOM uses multiple sensors because different sensors provide different types of environmental information.
| Sensor | Purpose | Position | Interface | Why selected |
|---|---|---|---|---|
| [PixyCam2] | [Detect coloured obstacles, visual track features, and navigation markers] | [In the front of chassi] | [USB connection to the Orange Pi; the program reads color detections using the Pixy2 camera library.] | [Performs fast colour/object processing and reduces processing demand on Orange Pi 5] |
| [SLAMTEC RPLIDAR C1] | [Measure surrounding distances, detect walls, estimate track position, and support obstacle avoidance] | [at the front of chassis and ontop of PixyCam 2] | [USB serial connection to the Orange Pi; the program reads scans through the LiDAR driver at 460800 baud.] | [Provides wide-area distance scanning instead of measurements from only a few fixed directions] |

### 4.4 Sensor calibration
Reliable autonomous navigation requires each sensing and control system to be calibrated before competition.

PixyCam2 Calibration

The PixyCam2 will be calibrated to recognise the colours and objects required by the competition.

Calibration will include:

defining colour signatures; adjusting colour thresholds; verifying recognition distance; testing different object positions; checking false detections; testing under different lighting conditions.

Lighting is particularly important because changes in brightness, shadows, reflections, and colour temperature can affect visual recognition.

The team will test the camera under several realistic indoor lighting conditions rather than relying on a single setup.

RPLIDAR C1 Calibration

LiDAR calibration will include checking:

measured distance against known physical distances; mounting orientation; angular reference position; minimum useful detection distance; measurement repeatability; areas blocked by the robot chassis.

Any systematic offset discovered during testing can be corrected in software.

Steering Calibration

Servo Horn Alignment and Center Point: The steering servo is centered mechanically by ensuring the servo horn is perpendicular to the steering linkage at a 90-degree pulse width (typically 1500 microseconds).

End-Point Limitation (PWM Bounds): We define maximum left and right steering angles in software to prevent mechanical binding, over-extension, or strain on the steering linkage and servo gear train.

Ackermann Steering Geometry Verification: The turning radius and steering arm linkages are physically inspected and tested to ensure smooth cornering response without wheel slip during tight maneuvers.

Verification: Command the steering to 0 degrees (center), left limit, and right limit via code, then visually check that the wheels align precisely to the target angles without motor humming or mechanical binding.

Drive Calibration
Drive Calibration must include the following:
Determining the minimum PWM signal required to overcome static friction and initiate motor rotation, ensuring zero-command signals result in a complete stop.

Calibrating the relationship between throttle input (PWM) and actual physical movement is tested across low, medium, and high duty cycles to ensure predictable acceleration profiles.

Verify these calibrations by slowly ramping up the motor PWM value from zero until the rear wheels begin continuous rotation, and record this threshold value to eliminate lag in the control code.

Data Storage Calibration
Data Storage calibration must include:
Ensuring all calibration constants—including steering trim offsets, minimum PWM thresholds, HSV color thresholds, and encoder ticks-per-meter—are stored locally in the ESP32's flash memory using Non-Volatile Storage (NVS) libraries.

Confirm that parameters are saved in structured configuration files or parameter dictionaries so they can be easily tuned, updated, or re-flashed without requiring structural changes to the core navigation codebase.

Verifying by power-cycling the microcontroller after saving new calibration parameters, then reading back the stored values via the serial monitor to confirm data persistence.

### 4.5 Wiring
The Monarch of Motion (MOM) uses a distributed electronic architecture consisting of an Orange Pi 5, ESP32, PixyCam2, SLAMTEC RPLIDAR C1, JGA25-370 drive motor, MG996 steering servo, and a single-battery power system.

The wiring documentation is stored in:

schemes/exported/wiring-diagram.png
schemes/exported/power-distribution.png
schemes/exported/system-block-diagram.png

The complete wiring diagram should show both power connections and signal connections.

## 5. Software architecture

### 5.1 Controllers and languages

MOM uses a two-controller architecture.
| System | Controller | Role | Language | Development Environment |
|---|---|---|---|---|
| High-level control | Orange Pi 5 | Navigation, sensor processing, decision-making, parking strategy, and system coordination | Python | Visual Studio Code |
| Low-level control | ESP32 | Drive motor control, steering control, and direct hardware interfacing | C++ | Visual Studio Code / ESP32 development environment |
| Visual sensor | PixyCam2 | Colour and object recognition | PixyCam firmware + Orange Pi interface | PixyCam tools / Python interface |
| Distance sensor | RPLIDAR C1 | 2D environmental distance scanning | Python interface | Visual Studio Code |

The Orange Pi 5 acts as the main decision-making computer, while the ESP32 acts as the real-time hardware controller.

This architecture separates computationally intensive tasks from time-sensitive motor and steering operations.

The Python software is developed in Visual Studio Code and organized into individual modules so that sensor reading, navigation, vehicle control and parking can be developed and tested independently.

Exact operating-system, Python, library and firmware versions will be recorded from the final competition system after the software environment has been frozen and successfully tested.

### 5.2 Module structure

The current Orange Pi software is located in:

src/

The current software files are:

| Module/File | Controller | Responsibility | Main Inputs | Main Outputs |
|---|---|---|---|---|
| `src/fusion_main.py` | Orange Pi 5 | Main system integration and navigation coordination | LiDAR data, PixyCam data, vehicle state | Navigation and movement decisions |
| `src/chassis_control.py` | Orange Pi 5 / ESP32 interface | Sends or manages drive and steering commands | Speed and steering targets | Motor and steering commands |
| `src/lidar_reader.py` | Orange Pi 5 | Reads and processes RPLIDAR C1 measurements | LiDAR scan data | Distance and environmental information |
| `src/basic_rplidar_c1.py` | Orange Pi 5 | Basic RPLIDAR C1 communication and testing | Raw LiDAR data | Diagnostic/test output |
| `src/pixy_reader.py` | Orange Pi 5 | Reads visual/object information from PixyCam2 | PixyCam object data | Detected object information |
| `src/pixycam2_basic.py` | Orange Pi 5 | Basic PixyCam2 connectivity and testing | PixyCam data | Diagnostic/test information |
| `src/parallel_park.py` | Orange Pi 5 | Autonomous parking behaviour | Position, sensor, and navigation data | Parking steering and drive commands |

### 5.3 Main program flow
The main control sequence is coordinated by fusion_main.py. At startup, it configures logging through log_config.py, launches scan_lidar.py and scan_pixy.py as sensor helper processes, and connects to the motor controller using serial_chassis.py. The LiDAR helper publishes recent distance measurements to a shared snapshot, while the Pixy helper publishes detected color blocks. During operation, fusion_main.py reads these snapshots to make navigation decisions. If it cannot connect to the chassis, it uses serial_utils.py to help identify available serial ports.

The program then repeatedly reads the latest sensor data. It first checks the LiDAR readings for a very close obstacle in front of the car; if one is found, the car briefly reverses and stops before continuing. Next, it checks orange and blue detections to count course corners and laps. These detections are mapped to color names using pixy_reader.py, and the lap-counting logic is in fusion_main.py. The car stops after the configured target of three laps.

For navigation, fusion_main.py selects red or green blocks detected by PixyCam2 and waits for repeated detections before acting, helping avoid turns based on a single unreliable frame. It passes a confirmed detection to pixy_calculations.py, which filters out track-like markings, estimates the obstacle’s distance from its image size, and calculates a steering plan. Red obstacles are passed on the left and green obstacles on the right. If an obstacle is too close, fusion_main.py briefly reverses before turning, then holds the chosen direction through temporary missed detections and drives straight briefly after the obstacle is passed.

When PixyCam2 has not recently identified a red or green obstacle, LiDAR acts as a fallback: fusion_main.py checks whether the front is blocked and, if so, compares the measured clearance on either side before turning toward a clearer path. The program continues checking the front path and returns to normal navigation once it is clear. A parallel-parking routine is implemented in parallel_park.py, but its pink-detection trigger is commented out in the current fusion_main.py, so it is not part of the active program flow. When the run ends or shutdown is requested, fusion_main.py stops the chassis and terminates the sensor helper processes.

### 5.4 Open Challenge strategy

For the Open Challenge, M.O.M. will rely primarily on the RPLIDAR C1 to make turning decisions. The LiDAR continuously measures distances around the robot. When readings indicate that the forward path is blocked, the control program compares the available space on the left and right and turns toward the clearer side, provided that side has enough measured clearance. If neither side appears sufficiently clear, the robot briefly reverses and stops rather than turning toward an uncertain path.

The PixyCam2 has a supporting role: it detects the orange corner markers so the program can track progress around the course. The robot counts the markers as corners, groups four corners into a lap, and stops when it reaches its configured lap target. In this strategy, visual marker detection supports course-progress tracking, while LiDAR provides the distance information used to select turns.

During a LiDAR-based turn, M.O.M. continues checking the front path and returns to normal driving when the path is detected as clear. A close-obstacle check also triggers a brief reverse when an object is detected within the emergency distance threshold.

### 5.5 Obstacle Challenge strategy

M.O.M.’s Obstacle Challenge strategy is to navigate the course using a reactive combination of camera and LiDAR data. The main program, fusion_main.py, continuously reads color detections from the PixyCam2 and distance readings from the RPLIDAR. The camera is used to recognize colored course objects and markers, while LiDAR provides distance information about obstacles and nearby open space.

When the PixyCam2 detects a red or green obstacle, the robot waits for repeated detections to reduce the chance of reacting to a single false reading. It then estimates the obstacle’s distance and position using pixy_calculations.py and plans a pass-by maneuver. The current code maps red obstacles to a left turn and green obstacles to a right turn. If the obstacle is too close for the maneuver, the robot reverses briefly before turning. It holds the selected turn through temporary camera dropouts, then drives straight briefly before resuming normal navigation.

LiDAR acts as a fallback when the camera has not recently identified a red or green obstacle. If the forward path is blocked, M.O.M. compares the measured clearance on each side and turns toward a side with enough space. If an obstacle is detected at very close range, the program commands a brief reverse. Meanwhile, orange and blue marker detections are used to count course corners; four corners make one lap, and the current program stops after three laps.

### 5.6 Control algorithms

The M.O.M. uses a reactive, sensor-based control algorithm rather than a PID controller or a preplanned route. During each control-loop iteration, fusion_main.py reads the latest PixyCam2 detections and refreshes the LiDAR snapshot. The program selects its next action from the current sensor readings and navigation state. It does not calculate a continuous speed or steering correction from a position-error value; instead, it issues discrete forward, reverse, turn, or stop commands.

Red and green obstacle avoidance combines PixyCam2 detection with image-based distance estimation. pixy_reader.py maps the camera’s signatures to color names and provides each block’s image position and size. The program filters out likely track markings and requires a red or green obstacle to appear in at least three of the most recent five frames before beginning an avoidance maneuver. In pixy_calculations.py, the apparent block size is used to estimate its distance, and its horizontal image position is converted to an approximate bearing. The algorithm then calculates a pass-by point beside the block and derives a steering command toward that point. The color determines the permitted passing direction: red is passed on the left, and green on the right. If the estimated distance is below the configured turn-ready distance, the car reverses before turning.

Once an avoidance turn begins, the controller enters an AVOID state and keeps the selected turn direction fixed. It can update the steering amount while the same obstacle remains visible, but a temporarily missed camera detection does not immediately cancel the turn. The program considers the obstacle passed after at least 0.8 seconds of turning and five consecutive frames without the target, or ends the maneuver at the 1.8-second timeout. It then enters a brief RECOVER state, driving straight for 0.25 seconds before returning to normal navigation. These state transitions help prevent abrupt steering changes caused by intermittent camera detections.

LiDAR obstacle avoidance acts as a fallback when PixyCam2 has not recently detected a red or green obstacle. The front is considered blocked when at least three readings in the forward 30-degree cone are at or below 600 mm. The controller then compares average valid distance readings in left and right sectors and turns toward a side whose calculated clearance meets the configured 300 mm minimum. If neither side has enough confirmed clearance, it reverses briefly and stops. While in LiDAR avoidance, the car keeps monitoring PixyCam2: two matching color detections can transfer control to the color-based avoidance algorithm. Otherwise, the LiDAR turn is held for the configured turn time, after which the car returns to normal navigation only if enough front readings indicate that the path is clear.

A separate close-obstacle check runs before the normal navigation decisions. If at least two front-cone LiDAR points indicate an obstacle within 150 mm, the program commands a brief reverse and stop. Lap counting is also handled in fusion_main.py: orange and blue detections are counted as course markers, with four corners counted as one lap; reaching the configured three-lap target stops the car.

Finally, serial_chassis.py converts each movement request into a serial steering/throttle pair for the chassis controller. Steering is represented by values from −100 to +100, where each unit corresponds to 0.5 degrees; throttle ranges from −100 (reverse) to +100 (forward), with 0 meaning stop. Thus, the control algorithm calculates which direction and speed command to send, while the chassis module handles transmitting that command.

### 5.7 Configuration values

The M.O.M. program uses configuration values to set the sensor connections, obstacle-detection thresholds, movement speeds, and navigation behavior. Most navigation settings are defined in fusion_main.py, while camera geometry and avoidance calculations are in pixy_calculations.py. The values below describe the current code and should be treated as tuning parameters; actual performance depends on the robot, sensor mounting, and course setup.

| Configuration | Current value | Purpose |
|---|---:|---|
| LiDAR serial port | `/dev/ttyUSB0` | Default port used to connect to the RPLIDAR. |
| LiDAR baud rate | `460800` | Serial communication speed used by the LiDAR helper. |
| Chassis serial port | `/dev/ttyS2` | Default port used to connect to the chassis controller. |
| Chassis baud rate | `9600` | Baud rate passed by the main program to the chassis module. |
| Pixy frame size and horizontal field of view | `316 × 208` pixels; `60°` | Camera geometry used to estimate an obstacle’s bearing and distance. |
| Estimated marker width | `50 mm` | Physical width assumed by the Pixy-based distance estimate. |
| Estimated chassis width | `146 mm` | Robot width used when calculating a safe pass-by point. |
| Passing clearance | `60 mm` | Additional space included in the pass-by calculation. |
| Steering range and scale | `−100` to `+100`; `0.5°` per unit | Steering command range; maximum steering corresponds to approximately `50°`. |
| Avoidance steering limits | `40`–`100` units | Minimum and maximum steering values for color-based avoidance. |
| Red/green detection confirmation | `3 hits in a 5-frame window` | Helps prevent a single noisy camera reading from triggering a turn. |
| LiDAR front-obstacle threshold | `600 mm` | Distance threshold used to identify a blocked front path. |
| LiDAR emergency threshold | `150 mm` | Very close obstacle threshold that triggers a brief reverse command. |
| Minimum LiDAR points for detection | `3`; `2` for emergency check | Requires multiple readings rather than relying on one isolated return. |
| Minimum side clearance | `300 mm` | Minimum clearance required for the LiDAR fallback to choose a side. |
| Forward, reverse, and turn speeds | `30`, `50`, and `30` | Chassis command speeds for normal driving, reversing, and color-based turns. |
| LiDAR fallback turn speed | `70` | Speed used during a LiDAR-initiated turn. |
| LiDAR fallback turn duration | `0.8 s` | Default turn duration; adjustable with `--turn-time`. |
| Pixy avoidance timing | Minimum `0.8 s`; maximum `1.8 s` | Minimum turn time and safety timeout for color-based avoidance. |
| Post-avoidance recovery | `0.25 s` | Time spent driving straight before returning to normal navigation. |
| Lap-counting configuration | `4` corners per lap; `3` target laps | Orange and blue marker detections counted toward the lap target. |
| Marker re-count interval | `1.5 s` | Prevents one continuously visible marker from being counted repeatedly. |

The main program also accepts command-line options for the LiDAR and chassis ports, serial baud rates, LiDAR turn time, minimum side clearance, and logging options. The LiDAR snapshot path can be changed with the LIDAR_DATA_PATH environment variable; marker width and chassis width can be changed with WRO_SIGN_WIDTH_MM and CAR_WIDTH_MM, respectively.

One configuration detail to verify during setup is the chassis baud rate: fusion_main.py currently passes 9600 by default, while serial_chassis.py defines 115200 as the class default. Because the main program passes its baud rate explicitly, the active default is 9600; it should match the ESP32 firmware configuration. 

## 6. Build and assembly instructions

Full instructions are in `docs/build-guide.md`

## 7. Software installation and operation

### 7.1 Required software

The Orange Pi 5 requires:

Linux-based Orange Pi operating system;
Python 3;
Visual Studio Code or another Python-compatible editor;
Git;
Python package manager (pip);
OpenCV;
NumPy;
RPLIDAR communication library/driver;
serial communication library where required;
PixyCam2 interface software/library.

The ESP32 requires an appropriate firmware development environment.

The exact versions used on the final competition vehicle will be frozen and documented before competition.

The repository contains:

requirements.txt

for Python dependencies.

Only libraries actually required by MOM should be included.

### 7.2 Installation

Clone the repository:

git clone [https://github.com/<GITHUB-USERNAME>/WRO-2026-The-Monarch-of-Motion](https://github.com/Envixious/WRO-2026-The-Monarch-of-Motion/).git

Enter the repository:

cd WRO-2026-The-Monarch-of-Motion

Create a Python virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Update pip:

python -m pip install --upgrade pip

Install dependencies:

pip install -r requirements.txt

The software can then be found in:

src/orange-pi/

The primary integration program is currently:

fusion_main.py

### 7.3 Uploading to Controllers

Orange Pi 5

The Python source code runs directly on the Orange Pi 5 and normally does not require compilation.

After cloning or updating the repository:

cd WRO-2026-The-Monarch-of-Motion/src/orange-pi

Run individual hardware tests first.

Examples:

python3 basic_rplidar_c1.py
python3 pixycam2_basic.py

After confirming sensor communication:

python3 fusion_main.py

The actual commands will be updated if the final program structure changes.

ESP32

The ESP32 firmware will be built and uploaded using the selected ESP32 development environment.

The final documentation will record:

ESP32 board model;
firmware framework;
compiler/platform version;
USB/serial settings;
required libraries;
upload procedure.

These details should match the exact competition controller and must not be guessed.

### 7.4 Running the Robot

The planned competition startup procedure is:

Place MOM in the required starting position.
Verify that the wheels and steering are unobstructed.
Switch on the computing-system battery.
Allow the Orange Pi 5 to complete startup.
Verify ESP32 communication.
Verify PixyCam2 connection.
Verify RPLIDAR C1 operation.
Load the required challenge configuration.
Confirm steering centre.
Confirm motor output is zero.
Start the navigation program.
Wait for the required start condition.
MOM begins autonomous operation.
At the end of the run, the vehicle stops automatically.
Stop the software safely.
Switch off the actuator power.
Switch off the computing power.

Any abnormal sensor or communication condition should result in the vehicle remaining stopped or entering the defined fault state.

###8. Testing and Engineering Validation
Testing was conducted to evaluate the performance of The Monarch of Motion (MOM), focusing on autonomous navigation, lap time, obstacle detection, steering, computing performance, and battery runtime. Parking and some additional tests remain incomplete because the robot has not yet progressed far enough through the course.

###8.1 Testing Results
| Test | Method | Runs | Metric | Result | Design Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Autonomous Laps** | Operated the robot on the track and observed its ability to complete laps autonomously. | 3 laps before stopping | Number of laps completed | The robot successfully completed 3 laps before stopping. Successful runs were consistent once the robot completed its intended movement. | Continue testing to evaluate reliability over longer runs and investigate why the robot stops after 3 laps. |
| **Lap Time** | Measured the time required to complete laps with and without obstacles. | 3 laps | Lap time (in minutes and seconds) | The robot completed a lap in approximately 2 minutes 20 seconds with obstacles and 1 minute 40 seconds without obstacles. | Improve navigation and obstacle-avoidance efficiency while maintaining reliable movement. |
| **Obstacle Detection** | Observed the robot's response to obstacles and checked PixyCam 2 line detection. | Observational testing | Obstacle detection reliability | The robot occasionally had difficulty detecting green obstacles. Some obstacles were outside the PixyCam 2's field of view. | Raised the PixyCam 2 to improve its viewing angle and visibility of the track. Further testing is needed to evaluate the improvement. |
| **Parking Accuracy** | Planned test involving autonomous entry into the designated parking area. | Not tested | Successful parking attempts | Not tested because the robot had not progressed far enough through the course to reach the parking stage. | Conduct parking tests once the robot can reliably complete the preceding sections of the course. |
| **Steering Performance** | Observed the robot's movement during left and right turns. | Observational testing | Ability to turn left and right | The robot can turn both left and right smoothly during observed operation. Reverse movement is available for repositioning when needed. | Continue testing turns on different sections of the track and adjust steering if inconsistencies occur. |
| **CPU Performance** | Observed the Orange Pi 5 Pro during robot operation. | Observational testing | Operational stability | No obvious CPU-related issues were observed during testing. CPU temperature and utilization were not formally measured. | Monitor CPU temperature and utilization during longer runs to confirm stable performance. |
| **Battery Runtime** | Observed the operating duration of the robot under normal usage. | Approximate observation | Operating time | The battery lasts approximately 1–2 hours, depending on operating conditions. | Record the runtime under a consistent condition to obtain a more accurate measurement. |
| **Lighting Conditions** | Used the PixyCam 2's built-in illumination during camera operation. | Observational testing | Line-detection performance | The PixyCam 2 uses its built-in lights to assist with visual detection. Performance under different ambient lighting conditions has not been formally measured. | Test the camera under different lighting conditions to evaluate detection consistency. |

###8.2 Evaluation
The results show that MOM can navigate the track, complete three laps, and perform left and right turns. The robot also demonstrates an approximate operating duration of 1–2 hours. However, obstacle detection remains an area for improvement, particularly when green obstacles are difficult for the PixyCam 2 to detect or fall outside its field of view.

To address this issue, the PixyCam 2 was raised to provide a better viewing angle. Further testing is required to determine whether this modification improves detection reliability. Parking accuracy has not yet been evaluated, and CPU performance and lighting reliability require more systematic measurements.

Future testing will focus on improving obstacle detection, investigating why the robot stops after three laps, and completing the parking stage. Additional repeated trials will help establish the robot's overall reliability and identify any remaining mechanical or software issues.

###9. Team Photographs
MOM's Team Photographs can be found in the t-photo.txt file in the repository

###10. Demonstration Video
MOM's Demonstration Video can be found in the Docs folder under team_videos.md

###11. Engineering Journal
Mechanical Iterations can be found in Docs/engineering-decisions.md

###12. Credits and External Resource
https://youtu.be/ulTM1uV1Bvg?si=4LF2zQf9gxllorqJ <- car assembly kit

MOM’s programming utilizes several external libraries to allow it to function:
| Library / package | Used for | Where it appears |
| :--- | :--- | :--- |
| **PySerial** (`serial`) | Serial communication with the chassis and port discovery. | `serial_chassis.py`, `serial_utils.py` |
| **Pixy2 Python library** (`pixy`) | Reading color-block detections from the PixyCam2. | `scan_pixy.py`, `pixy_reader.py` |
| **RPLIDAR driver** (`rplidarc1`) | Connecting to the RPLIDAR and reading scan data. | `scan_lidar.py` |

The project also uses Python’s standard library—for example, asyncio, pickle, argparse, and logging—and its own modules such as pixy_calculations.py.

###13. Contact
Teacher Email: nikhil.dsouza@binus.edu
