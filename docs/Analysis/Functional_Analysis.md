# **FUNCTIONAL ANALYSIS**

## Description of the production line

## Hardware components of the production line

- Dobot conveyor belt  
- 3 robots (2 Dobot Magician, 1 Dobot Magician Lite)  
- Laser sensor (object presence detection)  
- Color sensor (block color identification)

## Description of the operational flow

1. Robot R1 picks up a block from warehouse 1 (manual warehouse feeding by the operator) and places it on the conveyor belt.  
2. The laser sensor detects the passage of the block and signals the event to robot R2.  
3. Robot R2 intercepts the moving block and places it on the color sensor.  
4. Robot R3, which monitors the color sensor, detects a change in the color and retrieves the block from the color sensor, depositing it in warehouse 2 in the section corresponding to the detected color.

## Communication with the server

The ThingsBoard server will be hosted on a fourth PC (if a fourth PC cannot be used, one of the three will act as the server).  
Each robot has its own PC connected, running the program to send data to the ThingsBoard server.

## Anomaly management

- If the laser sensor does not detect any block passage within a predefined time interval, an error message is generated and sent to the control PC.  
- The PC then logs it in the database.

The system ensures full tracking of every production phase, from retrieval to final classification.

Go back to the [requirement analysis](./Requirement_Analysis.md)  
Continue with the [technical analysis](./Technical_Analysis.md)

Go back to the [index](./Analysis.md.md)
