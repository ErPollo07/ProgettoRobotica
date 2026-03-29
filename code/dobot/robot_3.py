# version: Python3
from DobotEDU import * # type: ignore
import time, requests


magician.set_color_sensor(port=2, enable=True, version=1) # type: ignore


class Point():
  """Represents a point in the system of the robot"""

  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z


### Configuration ###
SERVER_URL = "http://192.168.1.100:8080"

### Methods ###
def move_to_point(p: Point, mode: int = 0):
  """Move the robot to the coordinate of the point with a mode"""

  print(f"[TELEMETRY] Moving to ({p.x}, {p.y}, {p.z}) | mode = {mode})")
  magician.ptp(ptp_mode=mode, x=p.x, y=p.y, z=p.z, r = 0) # type: ignore


def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
  """Move the robot to the coordinate of the point  and the offset with a mode"""

  target_x = p.x + off_x
  target_y = p.y + off_y
  target_z = p.z + off_z

  print(f"[TELEMETRY] Moving to offset ({target_x}, {target_y}, {target_z}) | mode={mode}")
  magician.ptp(ptp_mode=mode, x=target_x, y=target_y, z=target_z, r = 0) # type: ignore


def suck(state: bool):
  """Set the suction cup on or off"""

  status = "ON" if state else "OFF"
  print(f"[TELEMETRY] Suction cup {status}")
  magician.set_endeffector_suctioncup(enable = state, on = state) # type: ignore


def get_color_sensor() -> dict:
  """Return the raw color sensor data"""
  return magicbox.get_color_sensor() # type: ignore


def get_color(color: str):
  """Return 1 if the specified color is detected"""
  return get_color_sensor()[color]


### HTTP Communication ###
def send_color_to_pc(color: str):
  """
  Send detected color to the PC server.

  Params
  ------
  color : str
    Detected color

  Returns
  -------
  bool, str
    True, None : If the command executed with error
    False, str : If the command had error
  """

  message = {
    "ts": str(time.time()),
    "robot_id": 3,
    "color": color
  }

  try:
    requests.post(f"{SERVER_URL}/robot/color", json=message)
    return True, None
  except Exception as e:
    return False, str(e)


def compute_color(values):
  if values == (1, 0, 0):
    return "red", WAREHOUSE_RED
  elif values == (0, 1, 0):
    return "green", WAREHOUSE_GREEN
  elif values == (0, 0, 1):
    return "blue", WAREHOUSE_BLUE
  else:
    return None, None

COLLECTION_POINT = Point(000, 000, 000)
IDLE_POINT = Point(000,000,000) # define an idle point (NOT ABOVE THE COLLECTION POINT)

WAREHOUSE_GREEN = Point(000,000,000)
WAREHOUSE_RED = Point(000,000,000)
WAREHOUSE_BLUE = Point(000,000,000)

### Main ###
def main():
  """
  When the robot detects a color, it sends it to the PC.
  The PC decides the destination and sends back a command.
  """

  # TODO Add a counter for how many blocks there are every warehouse (make a Warehouse class)

  # Declaring variables
  color: str | None
  point: Point | None

  move_to_point(IDLE_POINT)

  while True:
    color_detected = get_color_sensor()

    print(color_detected)

    # Check if any of the color is detected
    color, point = compute_color(tuple(color_detected.values()))

    if color != None and point != None:
      # wait 6 second (3 seconds more than the sleep of the robot 2) that the robot 2 release the block
      time.sleep(6)
      # status, error = send_color_to_pc(color)

      # collect the block
      move_to_point(COLLECTION_POINT)
      suck(True)

      # Put the block in the correct warehouse
      move_to_point(point)
      suck(False)

      move_to_point(IDLE_POINT)

      color, point = None, None


while True:
  main()
