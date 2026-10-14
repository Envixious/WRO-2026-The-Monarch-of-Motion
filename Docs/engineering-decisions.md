# Engineering decision log
Engineering Decisions
| Version | Change | Reason | Test evidence | Result |
|---|---|---|---|---|
| V1 | Moved the RPLidar 5 cm backwards from its original position in the middle of the car. | The original position caused cable-management issues, as the wires were too close to the wheels and could interfere with their movement | Visual inspection of the component placement and cable routing. | The RPLidar was repositioned to improve cable clearance, although further adjustments were still needed to optimize the wiring. |
| V2 | Moved the RPLidar to the front of the car. | The previous position did not provide the desired sensor placement. Moving it to the front was an attempt to improve obstacle detection, but the wiring still needed improvement | Inspection of the sensor's position and its surrounding components. | The front position was not suitable for the final layout, so the RPLidar was repositioned again in V3. |
| V3 | Moved the RPLidar 3 cm backwards. Moved the motor driver and buck converter underneath the chassis, between the motors. Moved the battery to the top of the chassis, between the RPLidar and Orange Pi 5 Pro. | The RPLidar was repositioned to improve component placement and weight distribution. The battery was moved to the top for easier replacement, while the motor driver and buck converter were moved underneath the chassis to improve cable management. | Inspection of component placement, wiring arrangement, and battery accessibility. | The new layout improved component organization and made the battery easier to access. Further driving tests would be needed to confirm improvements in stability. |
| V3.1 | Moved the PixyCam 2 to the top of the RPLidar. | Its original position at the front exposed it to potential collisions and limited its view of the ground. Moving it above the RPLidar was intended to improve ground-line visibility. | Inspection of the camera's mounting position and viewing angle. | The new position was intended to provide a clearer view of the ground and reduce the risk of direct collisions. Further testing would be needed to confirm improvements in line detection |

Engineering Journal
June 29, 2026 — Chassis Kit Assembly We began developing The Monarch of Motion (MOM) by assembling the chassis kit, which would serve as the mechanical foundation of our autonomous robot.

<img width="158" height="249" alt="image" src="https://github.com/user-attachments/assets/2195dbbf-9525-4178-bb3e-d77af79e30bf" />

The chassis provided the structure on which the motors, wheels, sensors, battery, and electronic components would eventually be mounted. Completing the initial assembly allowed us to begin planning the robot's component arrangement while considering the available space, cable routing, and weight distribution. These factors were important because the robot needed to remain within the WRO Future Engineers size requirements while maintaining sufficient stability for autonomous driving.

July 6, 2026 — Initial Wiring Diagram After assembling the chassis, we began planning the robot's electrical system by creating an initial wiring diagram. The diagram outlined how the electronic components would connect and helped us organize the power and signal connections before physically wiring the robot. Our system would include the Orange Pi 5 Pro, RPLidar, PixyCam 2, motor driver, buck converter or converters, and other components required for autonomous operation. Planning the connections in advance gave us a reference to follow during assembly and helped us identify how the different parts of the system would work together.

Wiring Diagram:
<img width="1600" height="830" alt="WhatsApp Image 2026-07-13 at 11 35 05 (1)" src="https://github.com/user-attachments/assets/37fcb7ae-8997-4957-8425-ed7fb9fc05ba" />


July 11, 2026 — Initial Component Weight Measurement

<img width="359" height="267" alt="image" src="https://github.com/user-attachments/assets/ec491321-a7e7-4cc9-8107-c8c09218ad9c" />

We measured the initial mass of the chassis assembly and recorded a weight of 776 g. We also considered the weight of the RPLidar and battery when evaluating how much additional mass the robot could accommodate. This was important for planning the placement of the remaining electronic components and ensuring that the completed robot would satisfy the competition's dimensional constraints. Establishing an initial weight measurement also gave us a reference for assessing the mass of the robot as more components were added.

July 13, 2026 — Finalization of the Wiring Diagram We revised the initial wiring diagram by adding labels to make the connections between components clearer and easier to follow.

<img width="783" height="387" alt="image" src="https://github.com/user-attachments/assets/ef460c84-f36c-403d-bd07-7b5e2e9dba46" />

During this revision, we also changed the power distribution design to use two buck converters instead of one. This required us to account for the updated arrangement in the wiring plan before proceeding with the physical assembly. Finalizing the diagram helped establish a more organized reference for soldering and connecting the electronic components in the following stages.

July 14, 2026 — Initial PixyCam 2 Training We began experimenting with the PixyCam 2 to understand how its color-recognition system worked and how it could support the robot's navigation.

<img width="447" height="365" alt="image" src="https://github.com/user-attachments/assets/fd3b29b3-e38e-45ae-b160-4d374f7874e7" />

During this session, we familiarized ourselves with the camera's training process and successfully configured it to recognize red and green objects. These initial experiments allowed us to explore its visual detection capabilities and understand how color information could be used to distinguish objects in the robot's environment.

July 18, 2026 — Autonomous Navigation Algorithm Development We began developing the robot's navigation algorithm, focusing on how the robot would interpret RPLidar readings and translate them into movement decisions.

<img width="330" height="247" alt="image" src="https://github.com/user-attachments/assets/ace29cbd-178a-461f-a38c-a1cb46373f71" />

Tasks were divided among team members so that different parts of the system could be developed in parallel. We worked on the motor-steering angles and the logic required to detect obstacles and determine how the robot should respond. This stage established the foundation for autonomous movement, in which the robot would use sensor information to navigate the track rather than relying on continuous manual control.

July 19, 2026 — PixyCam 2 Color-Detection Training We continued training the PixyCam 2 to recognize the colored objects used in our testing environment. By the end of the session, the camera could detect red and green LEGO blocks. This demonstrated that the camera could distinguish the selected colors and provided a foundation for using visual information during autonomous navigation. The PixyCam 2 would complement the RPLidar, which provides distance measurements rather than color identification, allowing the two sensors to contribute different types of information to the robot's navigation system.

July 25, 2026 — Track Preparation and Motor Grip Testing We obtained a printed WRO competition track map to prepare for testing the robot's movement and motor grip. The purpose was to investigate how the wheels would perform on the track surface and whether they could maintain sufficient traction during movement. However, we could not conduct the planned test because there was insufficient space for the testing setup. Consequently, the motor grip evaluation was postponed until a suitable testing environment could be arranged.

July 26, 2026 — RPLidar Simulation Testing We successfully connected the RPLidar to a simulator and investigated how it detected objects in its surroundings. Using a simulator allowed us to observe the sensor's readings without depending entirely on the completed physical robot. During this session, we identified a limitation involving transparent objects, which were not reliably detected. This was an important observation because the robot's obstacle-avoidance system depended on receiving sufficiently reliable distance information. Objects that the sensor could not detect consistently could potentially cause the navigation algorithm to make incorrect movement decisions.

RPLidar Simulation:
<img width="779" height="334" alt="image" src="https://github.com/user-attachments/assets/ee4996c3-39f7-420a-9e8f-35a2604e8d74" />


August 1, 2026 — Soldering the Power Connections

<img width="342" height="362" alt="image" src="https://github.com/user-attachments/assets/6a2fc966-c8cc-4e2b-84ad-f4467f6db815" />

We began soldering the robot's electrical connections, focusing on the wiring between the buck converter and the Orange Pi 5 Pro. These connections were necessary to integrate the power supply with the robot's computing system. We followed the previously prepared wiring diagram to guide the physical connections and maintain consistency between the planned circuit and the assembled hardware. This marked an important step in transitioning from the electrical design stage to the physical integration of the robot's electronic components.

August 2, 2026 — Orange Pi 5 Pro and PCB Integration We continued assembling the electronic system by soldering the connections between the Orange Pi 5 Pro and the printed circuit board (PCB).

<img width="133" height="185" alt="image" src="https://github.com/user-attachments/assets/8ad437ee-1b64-4820-ab8b-6b564f43800c" />

The wires were connected according to the finalized wiring diagram, which served as the reference for the physical implementation. Integrating the computing board with the PCB was necessary to bring the planned electrical system together and prepare the hardware for subsequent assembly and testing.

August 5, 2026 — Assembly of Version 1 (V1) We assembled the first version of the robot by securing the PCB and Orange Pi 5 Pro to the chassis using adhesive. The RPLidar was initially positioned near the middle of the car. However, the arrangement required further consideration because the wiring was close to the wheels and could potentially interfere with their movement.

<img width="190" height="353" alt="image" src="https://github.com/user-attachments/assets/9a8d0d5c-d7c4-45a3-80fe-6764dd4785d0" />

This highlighted the importance of evaluating the physical layout of the components alongside the electrical design. V1 provided our first assembled prototype and a starting point for identifying mechanical issues that needed to be addressed before more extensive testing.

August 14, 2026 — Preparation for RPLidar Testing We obtained walls to construct an obstacle-testing environment for the RPLidar:

<img width="307" height="295" alt="image" src="https://github.com/user-attachments/assets/d12295e4-b45b-407c-a324-5a422473c669" />

The planned tests were intended to investigate the sensor's ability to detect track boundaries and obstacles at different heights. However, the robot was still incomplete, so we could not carry out the intended testing session. We postponed the evaluation until the physical assembly was sufficiently complete to allow meaningful testing of the sensor in relation to the robot's actual dimensions and mounting position.

August 15, 2026 — Construction of a Makeshift Testing Track We constructed a makeshift track to begin evaluating the RPLidar's functionality in a physical environment. We used walls to investigate how the sensor detected boundaries at different heights and how their positions affected its readings. This allowed us to move beyond simulator-based observations and examine the sensor's behavior in relation to the robot's physical configuration. The observations from this testing session provided information that could be used to evaluate the sensor's mounting position and the robot's ability to detect its surroundings.

August 19, 2026 — Mechanical Issues with the RPLidar Mount (V2 Development) During development, we repositioned the RPLidar toward the front of the car, creating the V2 configuration. This change was intended to explore a more suitable sensor position for obstacle detection. However, the front-mounted arrangement introduced additional mechanical considerations, particularly concerning the acrylic platform supporting the sensor and the available clearance around the chassis. During testing, we observed that the robot could become stuck against this platform, indicating that the mounting structure interfered with its movement. This demonstrated that sensor placement needed to account not only for detection coverage but also for the physical clearance required for the robot to navigate the track.

August 19, 2026 — Investigation of RPLidar Navigation Issues During autonomous navigation testing, we also observed that the robot's RPLidar-based navigation algorithm could cause it to turn in the wrong direction in certain situations. We identified issues with the geometric calculations used to interpret sensor readings and determine the appropriate turning direction. In addition, the robot needed to update obstacle information more frequently and respond with faster turning movements. These findings showed that reliable navigation depended on both the quality of the sensor data and the accuracy of the algorithm interpreting that data. The problem therefore required further development of the robot's navigation logic.

August 24, 2026 — Mechanical Reassembly and Version 3 (V3) We disassembled and rebuilt the robot to improve component placement and overall mechanical efficiency. During this redesign, we moved the RPLidar 3 cm backwards from its front-mounted position in V2 to revise the sensor layout and weight distribution. We also moved the motor driver and buck converter underneath the chassis, between the motors, to improve cable routing and organize the electronic components more efficiently. The battery was relocated to the top of the chassis, between the RPLidar and Orange Pi 5 Pro, to make it easier to access and replace. These changes established the V3 configuration and addressed several practical considerations identified during earlier assembly and testing.

August 25, 2026 — Autonomous Navigation and Obstacle Challenge Testing We tested the robot on an obstacle-challenge track to evaluate how the PixyCam 2 and RPLidar worked together during autonomous navigation. The RPLidar provided distance information about surrounding obstacles, while the PixyCam 2 supplied visual information through color detection. Testing the sensors together allowed us to observe how the robot responded to the track environment and whether the combined sensing system supported its movement decisions. During testing, we identified occasional difficulties detecting green obstacles, particularly when they were outside the PixyCam 2's field of view. This indicated that the camera's mounting position and viewing angle required further consideration.

August 25–September 1, 2026 — PixyCam 2 Repositioning and Version 3.1 (V3.1) Following the obstacle-challenge testing, we repositioned the PixyCam 2 from the front of the robot to the top of the RPLidar, creating the V3.1 configuration. Its original position at the front exposed the camera to potential collisions and limited its view of the ground. Mounting the camera above the RPLidar was intended to provide a clearer viewing angle for ground-line detection while reducing the risk of direct physical interference. This modification was also intended to help address the detection difficulties observed during testing. However, further testing was still necessary to determine whether the revised mounting position improved line detection and the recognition of green obstacles.

September 1, 2026 — Navigation Logic Improvements We modified the robot's code to account for a scenario that had previously caused problems during autonomous operation. Earlier testing had revealed issues with the RPLidar-based navigation logic, including incorrect turning behavior caused by geometric calculations. The robot also needed to update obstacle information more frequently and respond with faster turning movements. This software revision was intended to improve the robot's decision-making when responding to the track environment. The updated code would need to be tested again to determine whether it resolved the original issue and whether any additional adjustments were necessary.

