# Camera

## Context

The robot 1 and 2 make all the movement that they have to do and they comunicate with each other in a virtual network using ZeroTier.
The only thing that is missing is the color sensor, that is the one that will be used to detect the color of the block in order to place it in the correct place.
But the color server is not working properly, so we need to find another way to detect the color of the block, and that is where the camera comes in.

## Objective

The objective of this feature is to use the camera to detect the color of the block and then send that information to the robot 2 so that it can place the block in the correct place.

## Implementation

The implementation of this feature will be done in the following steps:

1. Make a script that access the camera.
2. Use the video feed from the camera to detect the color of the block.
3. Modify the endpoint of the robots to receive the color information from the camera.
