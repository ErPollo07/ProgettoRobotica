# REQUIREMENT ANALYSIS

## Main objective

Simulate an automated production line using robots and save all data related to the production process in a database (ThingsBoard).

## Requirements

### Robot

The robots have to send telemetry data in real time during the work.
The telemetry that needs to be recorded is:

- Movement duration (this is common for all the robot): time needed to perform his action
- Infrared sensor event: when a block has been detected passing in front of the infrared sensor.
- Infrared sensor error: if no block passes within a predefined interval, an error event is logged to indicate a possible flow interruption
- Color sensor event: log the color of the block arrived at destination

### Local WEB server

The local web server is hosted in every pc that controls a robot.
These are the requirements for the server:

- Send and receive data with the robot
- Send the telemetry to a thingsboard server
- Store the telemetry sent by the robot in a json format
- Calculate the KPI (Key Performance Indicator):
  - Number of pieces produced per hour.  
  - Number of pieces produced, broken down by color.

### Thingsboard server

The Thingsboard server need to store all the telemetry of all the robots.
The Thingsboard server need to have two types of dashboards:

- General dashboard: Display the information about the KPI
- Robot dashboard: Display the information about one robot.

NB: There is one Robot dashboard for every robot.

Continue with the [functional analysis](./Functional_Analysis.md)

Go back to the [index](./Analysis.md.md)
