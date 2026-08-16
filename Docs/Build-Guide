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

## Mechanical assembly

1. [1. Prepare the Chassis

Prepare the main chassis according to the final MOM CAD design. Before installing any electronics, check:

chassis rigidity;
chassis dimensions;
mounting-hole alignment;
wheel clearance;
steering clearance;
motor clearance;
sensor mounting positions.

The final chassis material is TBC.]
2. [Install the Rear Drive System]
3. [Assemble the Front Ackermann Steering
MOM uses Ackermann steering controlled by one MG996-series servo.

Installation procedure:

Install the left and right front wheel steering assemblies.
Install the steering arms.
Install the tie rod / steering linkage.
Install the MG996-series servo. TBC
Connect the servo horn to the steering linkage.
Move the steering manually before powering the servo.
Confirm that both wheels can move left and right without obstruction.

Do not permanently fix the servo horn position until the electronic steering centre has been calibrated.

The following values are still TBC:

maximum left steering angle;
maximum right steering angle;
tie-rod length;
steering arm length;
final wheelbase;
front track width.]
4. [Install the Wheel
Install all four wheels.

Verify that:

all wheels rotate freely;
no wheel rubs against the chassis;
the front wheels can reach the required steering angles;
rear wheels remain aligned;
all wheel fasteners are secure.

Wheel diameter, width and tyre material are currently TBC.]

5. [Install the Orange Pi 5

Mount the Orange Pi 5 securely inside the chassis.

The Orange Pi should be positioned so that:

USB and other connectors remain accessible;
cooling airflow is not blocked;
wiring does not interfere with steering;
the board is protected from mechanical contact;
the centre of mass remains reasonably low.

The final Orange Pi mounting position is to be put at the center of the chassis.] 

6. [Install the ESP32

Mount the ESP32 close enough to the motor-control electronics to minimize unnecessary signal wiring.

The ESP32 should remain accessible for:

USB programming;
debugging;
wiring inspection.

Exact ESP32 board model and mounting position are the back of the chassis.]

7. [Install the RPLIDAR C1

Mount the SLAMTEC RPLIDAR C1 in a position with a clear horizontal scanning area.

The mount should:

hold the LiDAR rigidly;
minimize vibration;
avoid blocking the scanning plane;
keep cables away from the rotating/scanning area;
maintain repeatable orientation.

The final LiDAR mounting height is 6 cm]

8. [Install the PixyCam2

Mount the PixyCam2 toward the front of MOM.

The camera should have a clear view of:

approaching obstacles;
coloured pillars;
relevant track features.

The camera mount should allow the viewing angle to be adjusted during testing.

The final:

camera height 7 cm;
camera horizontal angle 360 degree;]

9. [Install the MPU6050 TBC]

10. [Install Battery Black Cell 1500 mAH]

## Electronics assembly
1. Disconnect all batteries.

Before performing any wiring:

Disconnect both batteries completely.

Never connect or modify wiring while the actuator power system is energized.

2. [Install the required:

voltage regulators;
power switches;
fuses;
connectors;
wiring;
distribution points.

The computing and actuator power systems should remain separated where appropriate.

The final regulator models and fuse ratings are TBC.]

