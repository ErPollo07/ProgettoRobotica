# Project plan

## Objectives

The objective of the project is to create a functional production chain with the robots.
At start of the production chain there is a robot that pick up blocks and put them in the conveyor belt.
In between of the first and the second robot there is a 3D printed conveyor guide that guide the block in the right position to be picked up from the second robot.
The second robot detect the movement of the block and proceed to pick up the block and put it above the color sensor. Then reposition it self above the collection point.
When the third robot detects a change in the sensor value it picks up the block and put it in the right warehouse for the color detected.

All the movements of the robots have to be registered in thingsboard.
The telemetry that have to be send to thingsboard is described in [Functional analysis](/docs/Analysis/Functional_Analysis.md#robot-specific-telemetry) document.

## Tasks for milestone

### Milestone 1: 03/03/2026

Guerra:

- Development of Robot 1 logic (block placement)
- Telemetry integration for R1

Tosatti:

- Development of Robot 2 logic (block interception)
- Laser sensor handling

Gaino:

- Development of Robot 3 logic (color detection and sorting)
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

## Verification and Validation Criteria

The project is considered successful if:

- All robots complete their assigned tasks without deadlocks.
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
