# TECHNICAL ANALYSIS

## Robot <-> PC Communication

To establish communication between the robot and the PC, an HTTP server has been implemented, hosted locally on the computer.  
The robot sends an HTTP POST request to the server at each significant event in the production line, sending a JSON payload containing the data of the executed operation (e.g., sensor status, coordinates, or action outcomes).

The server receives this data and immediately forwards it to the ThingsBoard platform via an HTTP request, allowing real-time monitoring of the system through IoT dashboards.

## Robot Code

The software running on the robots is designed to:

1. Handle the robot's operations on the production line materials.
2. Automatically report completed actions to the local server.

For each robot, we have created functions to assist with programming.  
For the Dobot Magician:

```python
def get_sensor_status() -> int:
  """
  Gets the infrared sensor status

  Returns
  ------
  int
    0 if the sensor doesn't detect anything
    1 if the sensor detects anything
  """
  return magicbox.get_infrared_sensor(port=2)["status"] # type: ignore
```

```python
def move_to_point(p: Point, mode: int = 0):
  """
  Move the robot to the coordinate of the Point with a mode

  Params
  ------
  p : Point
    The destination Point
  mode : int
    Specify the mode of movement:
      - 0: make a "jump" from the current position of the robot and the destination point
      - 1: go straight to the destination point
  """
  magician.ptp(mode, p.x, p.y, p.z, 0) # type: ignore
```

```python
def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
  """
  Move the robot to the coordinate of the Point and the offset with a mode.

  Params
  ------
  p : Point
    The destination Point
  off_x : float
    The offset to apply to the x of the destination point
  off_y : float
    The offset to apply to the y of the destination point
  off_z : float
    The offset to apply to the z of the destination point
  mode: int
    Specify the mode of movement:
      - 0: make a "jump" from the current position of the robot and the destination point
      - 1: go straight to the destination point
  """
  magician.ptp(mode, p.x + off_x, p.y + off_y, p.z + off_z, 0) # type: ignore
```

```python
def set_conv_speed(speed: int):
  """
  Set the conveyor speed.

  Params
  ------
  speed : int
    The speed to set to the conveyor.
  """
  magicbox.set_converyor(index=magicbox.STP1, enable=True, speed=speed) # type: ignore
```

```python
def suck(state: bool):
  """
  Set the suction cup on or off.

  Params
  ------
  state : bool
    The state that needs to be applied to the suction cup.
  """
  magician.set_endeffector_suctioncup(enable=state, on=state) # type: ignore
```

Per i dobot magician lite:

```python
def move_to_point(p: Point, mode: int = 0):
  m_lite.set_ptpcmd(ptp_mode=mode, x=p.x, y=p.y, z=p.z, r=0)# type: ignore
```

```python
def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
  m_lite.set_ptpcmd(ptp_mode=mode, x=p.x + off_x, y=p.y + off_y, z=p.z + off_z, r=0) # type: ignore
```

```python
def suck(state: bool):
  m_lite.set_endeffector_suctioncup(enable=state, on=state) # type: ignore
```

## Server Code

The server is implemented as a local web server within the network.  
Its main function is to receive the HTTP requests sent by the robots, process the JSON payloads, and forward them to ThingsBoard or other internal endpoints.

Go back to the [functional analysis](./Functional_Analysis.md)

Go back to the [index](./Analysis.md.md)