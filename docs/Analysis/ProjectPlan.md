# Project plan

## Objectives

The goal of the project is to create a functional production chain with robots and a camera.
At the beginning of the production chain, a robot picks up the blocks and places them on the conveyor belt.
Between the first and second robots, there is a 3D-printed conveyor belt guide that guides the block into the correct position for pickup by the second robot.
The second robot detects the block's movement, picks it up, and places it over the color sensor. It then repositions itself over the pickup point.
When the camera detects a change in color value, it sends a message to the second robot with the detected color.

All robot movements must be recorded in Thingsboard.
The telemetry to be sent to Thingsboard is described in the document [Functional Analysis](/docs/Analysis/Functional_Analysis.md#robot-specific-telemetry).

## Tasks for milestone

### Milestone 1: 03/03/2026 - Funzionalita' di base

Guerra:

- Development of Robot 1 logic (block placement)
  The robot have to place take blocks from a collection point and place it on the conveyor belt.
- Telemetry integration for R1

Tosatti:

- Development of Robot 2 logic (block interception)
  The robot detects when a block passes in front of the laser and pick it up and place it above the color sensor.
- Laser sensor handling

Gaino:

- Development of Robot 3 logic (color detection and sorting)
  The robot have to get the color from the color sensor.
  If the color change (so from nothing it detects a color) the robot have to take the block and put the block in a predifined point.
- Color sensor integration

### Milestone 2: --/--/----

Guerra:

- Movement timing measurement

Tosatti:

- Infrared error detection

Gaino:

- Color-based warehouse management

### Milestone 3: --/--/----

Gaino:

- Send telemetry to thingsboard

Guerra:

- Send telemetry to thingsboard

Tosatti:

- ThingsBoard configuration and dashboard creation

## Program changes

As the project progressed, a change was made: the R3 robot was replaced with a camera because the color sensor connected to the robot did not always detect colors accurately.

## Verification and Validation Criteria

The project is considered successful if:

- All robots complete their assigned tasks without deadlocks.
- The camera detects colors perfectly and distinguishes them.
- Every movement generates telemetry.
- Laser and color events are logged correctly.
- KPIs are correctly calculated.
- Anomalies are recorded and visible on dashboards.
- No critical production interruption occurs during testing.

Validation methods:

- Functional testing of each robot
- Integration testing of full pipeline
- Dashboard consistency checks
- Manual anomaly injection tests

## Design Risks

 - Availability of a backup robot for use in the event of malfunctions, maintenance requirements,
 or unexpected changes to the execution program. Use of dedicated laptops, pre-configured with the necessary software environment, to reduce setup times and ensure operational continuity. 
 Provision of alternative connections via mobile hotspots to ensure business continuity
 in the event of internet failure or instability.  

 - Unreliable behavior of the camera-based color detection system due to environmental conditions (lighting variations, shadows, reflections) or hardware limitations, leading to incorrect or unstable color classification.  

 - Concurrent access issues between multiple hardware components (camera, robot controller, and auxiliary processes), potentially causing resource conflicts, blocking behavior, or device access failures.  

 - Latency and overload risks in the local Flask server, especially when handling computationally expensive operations such as real-time color detection requests, which may affect system responsiveness.  

 - Inconsistencies between different sensing modalities (infrared sensor and camera system), which may lead to conflicting interpretations of the same physical state and ambiguous decision-making in the control logic.  

 - Instability caused by fixed threshold-based classification in the vision system, which may lead to oscillating or unreliable detections under borderline conditions.  

 - Failures or resource leaks in OpenCV video capture due to driver issues, device disconnection, or improper release of camera resources, potentially causing frozen processes or memory leaks.  

 - Incompatibilities across different software environments (Python, OpenCV versions, system drivers), which may lead to inconsistent execution behavior between development and deployment systems.  

## Mitigation Strategies

 - Availability of a backup robot for use in the event of malfunctions, maintenance requirements, or unexpected changes to the execution program.
 Use of dedicated laptops, pre-configured with the necessary software environment, to reduce setup times and ensure operational continuity.
 Provision of alternative connections via mobile hotspots to ensure business continuity in the event of internet failure or instability.  

 - Application of HSV-based color segmentation techniques to improve robustness of the vision system against lighting variations, combined with confidence thresholds to filter unreliable detections and a fallback state when detection is not confident.  

 - Use of a singleton pattern and synchronization mechanisms (locks/mutexes) to prevent concurrent access conflicts to shared hardware resources such as the camera and robot interfaces.

 - Definition of a hierarchical sensor fusion strategy, prioritizing infrared sensor readings for triggering actions while using camera-based detection as secondary enrichment, combined with timestamp-based correlation of events.  

 - Introduction of hysteresis thresholds and temporal smoothing (e.g., multi-frame averaging or sliding window majority voting) to stabilize vision-based classification and reduce oscillations.