# Robot build and reproduction guide

This guide explains how to assemble, wire, install, calibrate, and prepare The Monarch of Motion (MOM) for operation in the WRO 2026 Future Engineers competition.

The current MOM design uses:

Orange Pi 5 as the main high-level controller
ESP32 as the low-level hardware controller
PixyCam2 for visual/object detection
SLAMTEC RPLIDAR C1 for 2D distance sensing
MPU6050 IMU — optional / TBC
1 × JGA25-370 geared DC motor for rear-wheel drive
1 × MG996-series servo for Ackermann steering
Dual-battery power system
Python as the main Orange Pi programming language
Visual Studio Code as the primary development environment

Current vehicle dimensions are approximately:

Length: 250 mm
Width: 170 mm
Height: 100 mm

## Tools required
[The following tools are currently expected to be required for building and maintaining MOM.

Mechanical Tools
Small Phillips screwdriver set
Small flat-head screwdriver
Hex / Allen key set — exact sizes TBC
Small spanner / wrench set — exact sizes TBC
Needle-nose pliers
Side cutters
Wire stripper
Vernier caliper
Metric ruler
Small file / deburring tool
Hobby knife
Tweezers
Cable ties
Thread-locking compound — optional / TBC
Electronics Tools
Digital multimeter
Heat-shrink tubing
Electrical tape
Dupont / JST crimping tool — connector type TBC
USB cables for Orange Pi 5 and ESP32
ESP32 programming cable — exact connector TBC
Fabrication Tools

Depending on the final chassis and mounting design:

Computer / Programming Tools
Laptop or desktop computer
Visual Studio Code
Git
GitHub
Python 3
Python pip
ESP32 programming environment — TBC
PixyCam2 configuration software
RPLIDAR testing/software tools as required
]

## Parts required
See `bill-of-materials.csv`.

# Base Car 
1. Attach the 12mm bearing into the back side of the steering cup 2. Attach the 8mm bearing into the front side of the steering cup 3. Insert the drive shaft through the 12mm bearing on the back side of 
the steering cup, in which they’ll exit through 8mm bearing on the front side of the steering cup 
4. Attach the hexagonal adapters to the drive shaft, with the pole being inserted through the hole close to the 8mm bearing, and the hexagonal adapter itself being inserted through the drive shaft 
5. Attach the 65mm wheels to the steering cup via hexagonal adapter, securing it with the provided nut. 
6. Set one (1) of the transmission links to exactly 6.3cm, ensuring accuracy with a ruler. Set the other transmission link to exactly 4.6cm. 7. Attach one end of the transmission link (6.3cm) to the top hole located on the steering cup, while attaching the other end to the other steering cup. Ensure that the steering cups mirror one another. 8. With the transmission link (6.3cm) facing down, attach the other transmission link (4.6cm) to the right steering cup on the hole directly under where the 6.3cm transmission link is connected. 9. Next, attach the MG996R L-Bracket to the MG996R actuator, with the tail end facing away from the front of the motor. 
10. Set the MG996R actuator to 0 degrees, before attaching the Servo Horn facing upwards. Secure the Servo Horn with a screw. 
11. Then, attach the JGA25-370 Motor to the L Mount Bracket. 12. Take the Rear-Wheel Link and attach the 17 MILLIMETERS D-5MM coupling, the longer coupling attached to the side with the longer flat end. (The shorter coupling attached to the side with the shorter flat end) 13. However, before attaching the other 17 MILLIMETERS D-5MM coupling, slip on the Flanged Bearings, with the flared side pressed against the coupling. 
14. Slip the Rear-Wheel Link through the L Mount Bracket (left to right), before slipping on the other Flanged Bearing, the flared side facing outward. 
15. Attach the provided wide gear onto the JGA25-370 Motor, while the provided small gear on to the right side of the link. 
16. Slip on the 17 MILLIMETERS D-5MM coupling, on top of the small gear. 
17. Finally, attach the MG996R and the JGA25-370 Motor to the metal chassis
(If you need more visual aid, refer to this video, from 0:00-23:06) 
NOTE: DO NOT ADD THE GOLD PILLARS, OTHER THAN THE ONES REQUIRED FOR THE FRONT WHEELS 

# Electronics and Sensor Assembly 
1. Prepare the buck converters and motor driver. Solder the two (2) buck converters and the motor driver together according to the wiring diagram provided in the wiring documentation. Check that all connections match the diagram before proceeding. 
2. Connect the electronics to the Orange Pi. Connect the motor driver and other required control connections to the Orange Pi 5 Pro, following the wiring documentation. 
3. Connect the motor driver to the motors. Connect the motor driver outputs to the JGA25-370 motors according to the wiring diagram. Ensure that the motor connections are correctly positioned and secured. 
4. Connect the buck converters to the battery plug. Connect the buck converters to the battery power plug according to the wiring documentation. Check the polarity and connections before connecting the battery. 
5. Mount the buck converters and motor driver. Position the buck converters and motor driver underneath the metal chassis, in the space between the motors. Arrange the components to minimise cable tangling and prevent wires from interfering with the wheels or moving parts. 
6. Mount the Orange Pi 5 Pro. Position the Orange Pi 5 Pro at the rear of the metal chassis. Ensure that the USB ports face the rear of the vehicle so that the LiDAR can be connected easily. 
7. Install the front LiDAR mounting pillars. Attach two (2) gold pillars near the front wheels using the provided screws. These pillars will support the RPLidar C1 mounting assembly. 
8. Build the central acrylic platform. Attach four (4) additional gold pillars to the chassis to support the provided acrylic platform in the middle of the vehicle. Secure the acrylic piece onto the pillars using the provided screws. 
9. Mount and connect the RPLidar C1. Use thick, grey double-sided mounting tape to secure the RPLidar C1 to its designated mounting position near the front of the chassis. Route the LiDAR cables underneath
the sensor and secure them to the mounting pillars using cable ties. Connect the LiDAR to one of the USB ports at the rear of the Orange Pi 5 Pro. 
10. Mount and connect the PixyCam 2. Attach the PixyCam 2 to the custom 3D-printed mounting bracket. Use thick, grey double-sided mounting tape to secure the bracket on top of the RPLidar C1. Connect the PixyCam 2 to the Orange Pi 5 Pro according to the wiring documentation. Route the camera cables along the chassis and secure them to the mounting pillars using cable ties to prevent them from interfering with moving components. 
11. Install the protective acrylic cover. Position the remaining acrylic piece above the central platform to protect the Orange Pi 5 Pro. Secure the acrylic piece to the platform using cable ties, ensuring that the computer and its cables remain accessible where necessary. 
Note: Refer to the wiring documentation for all electrical connections. Ensure that the cables are secured away from the wheels, gears, and other moving components before powering on the vehicle.

<img width="787" height="398" alt="image" src="https://github.com/user-attachments/assets/2d07a888-c169-4558-b06a-d855ea699e01" />
