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

MOM has compact dimensions of **250 mm in length, 170 mm in width, and 100 mm in height**. These dimensions remain within the WRO maximum vehicle size of **300 mm × 200 mm × 300 mm**. Its low-profile design helps lower the centre of gravity, improving stability during cornering and reducing unnecessary body movement.

The vehicle uses a **rear-wheel-drive system powered by one JGA25-370 DC geared motor**. This configuration complies with the WRO rule allowing a maximum of one drive motor. Rear-wheel drive provides a simple and efficient mechanical arrangement while leaving the front section available for the steering mechanism and sensors.

Steering is controlled by one **MG996 servo motor** connected to an **Ackermann steering system**. This also complies with the WRO rule permitting a maximum of one steering motor. Ackermann steering allows the inner and outer front wheels to turn at different angles during a corner, reducing tyre slip and improving turning accuracy.

The main processing system consists of an **Orange Pi 5** and an **ESP32**. The Orange Pi 5 functions as the vehicle’s main computer or “brain.” It is responsible for high-level tasks such as sensor processing, obstacle detection, navigation decisions, route planning, and competition strategy. The ESP32 functions as the real-time control unit. It receives instructions from the Orange Pi 5 and controls the drive motor, steering servo, and other low-level hardware functions.

The software is developed using **Visual Studio Code** with **Python** as the main programming language. Python is used because it supports rapid development, sensor integration, computer vision, data processing, and clear modular programming. The ESP32 may use separate firmware for direct motor and servo control, while communication between the Orange Pi 5 and ESP32 allows the system to separate high-level decision-making from time-sensitive hardware control.

For visual detection, MOM uses a **PixyCam2**. The camera is intended to identify important visual features such as coloured obstacles, track elements, and navigation markers. Because PixyCam2 performs some image processing internally, it can reduce the processing workload placed on the Orange Pi 5.

A **SLAMTEC RPLIDAR C1** provides distance measurements around the vehicle. The LiDAR can be used to detect walls, estimate the vehicle’s position relative to track boundaries, measure available space, and support obstacle avoidance. Its wide scanning range gives the vehicle more environmental information than a small number of fixed distance sensors.

An **MPU6050 inertial measurement unit**, which is currently still to be confirmed, may be added to provide gyroscope and acceleration data. It could help detect changes in orientation, estimate turning movement, and support more stable navigation. However, the final use of the MPU6050 will depend on testing and whether it provides a meaningful improvement over the existing camera and LiDAR system.

MOM uses a **dual-battery system**. The batteries can supply the computing system and the motor system separately. This reduces the possibility that electrical noise or sudden current demand from the drive motor and steering servo will interrupt or restart the Orange Pi 5. The final electrical design will include suitable voltage regulators, shared grounding, switches, fuses, and battery monitoring.

## Main Strengths

One of the main strengths of MOM is its **hybrid control architecture**. The Orange Pi 5 handles complex navigation and sensor-processing tasks, while the ESP32 manages direct hardware control. This division reduces the workload on each controller and allows the motor and steering system to respond quickly even when the Orange Pi 5 is processing camera or LiDAR data.

The combination of the **PixyCam2 and RPLIDAR C1** gives the robot two different types of environmental information. The camera can classify coloured objects, while the LiDAR can measure distance and detect surrounding structures. Using both sensors may improve reliability because the robot is not dependent on only one sensing method.

The vehicle’s **compact and low-profile chassis** is another advantage. Its dimensions provide sufficient space for the electronics while remaining comfortably inside the WRO size limits. The low height may improve stability and reduce the risk of excessive body movement during fast turns.

The **Ackermann steering mechanism** provides more realistic and controlled cornering than a simple parallel steering linkage. It can reduce wheel scrubbing, improve turning consistency, and allow better control of the vehicle’s path around corners.

The **rear-wheel-drive layout** is mechanically simple and allows the front wheels to focus only on steering. This separation may make the vehicle easier to maintain, calibrate, and troubleshoot.

The **dual-battery system** can improve electrical reliability by separating sensitive computing components from motors and servos that produce voltage drops and electrical noise. This is particularly important because the Orange Pi 5 requires a stable power supply.

## Current Limitations

The most significant limitation is the **complexity of integrating several controllers and sensors**. The Orange Pi 5, ESP32, PixyCam2, RPLIDAR C1, motor driver, servo, and possible MPU6050 must communicate reliably. Communication delays, incorrect data formats, disconnected cables, or software crashes could affect the entire vehicle.

The **Orange Pi 5 has relatively high power consumption** compared with a small microcontroller. It may also produce heat during continuous image processing and LiDAR data processing. The vehicle therefore requires effective voltage regulation, cooling, cable management, and power monitoring.

Although the dual-battery system can improve reliability, it also increases the **weight, wiring complexity, and charging requirements** of the robot. Both batteries must be secured safely, monitored separately, and checked before every run. Incorrect grounding between the two power systems could also cause communication problems.

The **PixyCam2 may be affected by lighting conditions**, reflections, shadows, and colours similar to the competition obstacles. Its performance will depend on careful colour calibration and repeated testing under different lighting environments.

The **RPLIDAR C1 adds weight and requires a clear scanning area**. Its measurements may also be affected by vibration, reflective surfaces, incorrect mounting, or temporary obstruction by parts of the robot. Processing a large amount of LiDAR data may increase the load on the Orange Pi 5.

The proposed **MPU6050 may experience sensor drift**, especially when estimating direction over a long period. It should not be used as the only source of orientation information. Its data may need filtering and correction using camera, LiDAR, or track-reference information.

The **MG996 servo can draw a high current**, especially when the steering mechanism is under load. It may also have mechanical backlash, which can reduce steering precision. The steering linkage must therefore be rigid, correctly aligned, and carefully calibrated.

Using only one JGA25-370 drive motor creates a **single point of failure**. If the motor, gearbox, wheel connection, or motor driver fails, the vehicle cannot move. Rear-wheel drive may also experience reduced traction during rapid acceleration, sharp turning, or movement on a dusty competition surface.

Finally, the chassis height of only 70 mm creates **limited internal space**. Components must be arranged carefully to prevent cable interference, overheating, blocked LiDAR scans, restricted airflow, or contact between moving steering parts and electronic components.

Overall, MOM has a strong foundation because it combines a compact mechanical platform, Ackermann steering, rear-wheel drive, high-level computing, real-time motor control, camera detection, and LiDAR sensing. Its final performance will depend on careful integration, power management, calibration, repeated testing, and simplification of any system that does not provide a clear improvement in reliability.]

## 2. Repository contents

- `docs/` — engineering journal, build guide, bill of materials, decisions, risks, testing, and releases.
- `t-photos/` — team photographs.
- `v-photos/` — vehicle photographs from front, rear, left, right, top, and bottom.
- `video/` — YouTube links for autonomous demonstrations of both challenges.
- `schemes/` — wiring, power, electronic, and system architecture diagrams.
- `src/` — complete source code for every programmed controller.
- `models/` — editable CAD files and exported STEP/STL manufacturing files.
- `other/` — datasets, datasheets, setup notes, and other reproducibility materials.

## 3. Mobility and mechanical design

### 3.1 Chassis

The Monarch of Motion (MOM) uses a compact chassis designed specifically for the WRO Future Engineers competition. The current vehicle dimensions are approximately 250 mm in length, 170 mm in width, and 100 mm in height. These dimensions remain within the WRO maximum vehicle dimensions of 300 mm × 200 mm × 300 mm.

The relatively low vehicle height helps maintain a low centre of mass, which improves stability during cornering and reduces unnecessary body movement when the vehicle changes direction. The compact chassis also provides sufficient space for the drive system, steering mechanism, Orange Pi 5, ESP32, PixyCam2, RPLIDAR C1, batteries, and other electronic components.

The vehicle uses a rear-wheel-drive layout with the steering mechanism located at the front. The front section contains the Ackermann steering system and provides mounting positions for navigation sensors. The Orange Pi 5, ESP32, batteries, and power electronics are positioned within the main chassis area to keep the vehicle balanced.

The exact chassis material, total vehicle weight, wheelbase, track width, and measured centre-of-mass position are still being finalized and will be recorded after the final mechanical design is completed.

Current chassis specifications:

Specification	Value
Length	250 mm
Width	170 mm
Height	100 mm
Maximum WRO length	300 mm
Maximum WRO width	200 mm
Maximum WRO height	300 mm
Vehicle weight	TBC
Wheelbase	TBC
Front track width	TBC
Rear track width	TBC
Chassis material	TBC
Centre of mass	TBC

The mounting system is designed to keep the major components securely attached while maintaining enough rigidity to prevent unwanted chassis flex. Particular attention is given to the steering mechanism and sensor mounts because movement or vibration in these areas could reduce navigation accuracy.

### 3.2 Drive mechanism

MOM uses a rear-wheel-drive system powered by one JGA25-370 DC geared motor. The use of one drive motor complies with the WRO Future Engineers requirement allowing a maximum of one motor for propulsion.

The motor is installed at the rear section of the vehicle and transfers power to the rear drive system. Rear-wheel drive was selected because it provides a relatively simple mechanical arrangement and allows the front wheels to be used entirely for steering.

Separating propulsion and steering also simplifies control. The drive motor is responsible for forward and reverse movement, while the front Ackermann steering system controls the vehicle's direction.

The JGA25-370 was selected because geared DC motors of this type provide a useful balance between torque, speed, compact size, and controllability for a small autonomous vehicle.

The final motor driver, gearbox ratio, wheel diameter, encoder specification, and exact transmission arrangement will be documented after the drive system is fully finalized and tested.

Current drive-system specifications:

Specification	Current design
Drive layout	Rear-wheel drive
Drive motor	1 × JGA25-370 DC geared motor
Number of drive motors	1
Gear ratio	TBC
Wheel diameter	TBC
Encoder	TBC
Motor driver	TBC
Controller	ESP32
High-level controller	Orange Pi 5

The ESP32 will provide the low-level motor-control commands, while the Orange Pi 5 will determine the required vehicle movement based on information from the navigation sensors.

This configuration was preferred over a more complicated drivetrain because MOM requires reliable and repeatable movement rather than maximum vehicle speed.

### 3.3 Steering mechanism

MOM uses an Ackermann steering system operated by one MG996 servo motor. The use of a single steering servo complies with the WRO requirement permitting a maximum of one motor for steering.

Ackermann steering allows the inner and outer front wheels to turn through different angles while cornering. The inner wheel follows a smaller turning radius than the outer wheel. This reduces tyre scrubbing and allows the vehicle to follow a smoother path through corners.

The MG996 servo controls the steering linkage mechanically connected to the front wheels. The servo receives steering commands from the ESP32, while the steering target is determined by the Orange Pi 5 navigation system.

The steering system will be calibrated around three important reference positions:

centre or straight-ahead position;
maximum safe left steering position;
maximum safe right steering position.

Software limits will be used to prevent the servo from attempting to move beyond the safe mechanical steering range. Mechanical limits will also be considered to prevent excessive movement of the linkage or contact between steering components and the chassis.

The exact steering-angle range will be measured after the final steering linkage is assembled.

Current steering specifications:

Specification	Current design
Steering geometry	Ackermann
Steering motor	1 × MG996 servo
Steering controller	ESP32
Centre position	To be calibrated
Maximum left angle	TBC
Maximum right angle	TBC
Mechanical stops	To be finalizedx
Software steering limits	To be calibrated

Ackermann steering was selected because the WRO track contains repeated corners and requires accurate vehicle positioning. Reduced wheel slip should provide better consistency when MOM navigates both the Open Challenge and Obstacle Challenge.

### 3.4 Torque and speed reasoning

TBC

### 3.5 Mechanical iterations

| Version | Change | Reason | Test evidence | Result |
|---|---|---|---|---|
| V1 | [CHANGE] | [WHY] | [TEST] | [RESULT] |
| V2 | [CHANGE] | [WHY] | [TEST] | [RESULT] |
| V3 | [CHANGE] | [WHY] | [TEST] | [RESULT] |

## 4. Power and sensor architecture

### 4.1 Power system
TBC

### 4.2 Power budget
| Component | Voltage | Typical current | Maximum current | Power source |
|---|---:|---:|---:|---|
| [Orange Pi 5] | [5 V] | [To be measured on MOM] | [4 A supply capacity] | [Computing-system battery] |
| [ESP 32] | [3.3 V] | [~95–100 mA receiving; up to ~240 mA during high-power Wi-Fi TX] | [≥500 mA recommended supply capacity] | [Regulated computing supply] |
| [SERVO] | [V] | [A] | [A] | [SOURCE] |
| [Motor] | [V] | [A] | [A] | [SOURCE] |
| [PixyCam2] | [5 V regulated] | [140 mA] | [Manufacturer does not specify a formal maximum] | [Computing-system battery] |
| [RPLIDAR C1] | [5 V] | [230 mA] | [260 mA running; ~800 mA at startup] | [Computing-system battery] | 
| [Motor] | [V] | [A] | [A] | [SOURCE] |

### 4.3 Sensors and placement

MOM uses multiple sensors because different sensors provide different types of environmental information.
| Sensor | Purpose | Position | Interface | Why selected |
|---|---|---|---|---|
| [CAMERA] | [PURPOSE] | [POSITION] | [INTERFACE] | [REASON] |
| [DISTANCE SENSOR] | [PURPOSE] | [POSITION] | [INTERFACE] | [REASON] |
| [ENCODER/IMU] | [PURPOSE] | [POSITION] | [INTERFACE] | [REASON] |
