# Robot setup

## Cables

Below are all the connections from the robot to other devices:

- PC: USB-B
- Suction Cup: GP1, SW1
- Laser: GP2
- Conveyor: Stepper1

The magic box is not required for operation.

## Connection Problems

If the robot does not appear in the top-right corner after installing Dobot Link, or if you receive errors when clicking connect, the issue is likely a driver problem. To resolve this:

1. Connect the USB cable and open Device Manager
2. Look for an unknown device under "Other devices"
3. Install the appropriate driver for that device

## Robot Position

The robot and conveyor must be placed next to each other to avoid alignment problems. Position them as shown in the diagram below:

```txt
                    *---------------*
                    |               |
                    |               |
                    |     ROBOT     |
                    |               |
                    |               |
                    *---------------*
    *------------------------------------------------*
    |                                                |
    |                                                |
    |                  CONVEYOR                      |
    |                                                |
    |                                                |
    *------------------------------------------------*
```

There should be no gap between the conveyor and the robot.
