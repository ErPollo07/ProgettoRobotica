# version: Python3
from DobotEDU import *
import requests
import time


magician.set_color_sensor(port=2, enable=True, version=1)


class Point():
  """Represents a point in the system of the robot"""

  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z


### Configuration ###
SERVER_URL = "http://192.168.1.100:5000"


### Methods ###
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
      - 1: go strait to the destination point
  """
  magician.ptp(mode, p.x, p.y, p.z, 0) # type: ignore


def get_color_sensor():
  """Return the raw color sensor data"""
  return magicbox.get_color_sensor()


def get_color(color: str):
  """Return 1 if the specified color is detected"""
  return get_color_sensor()[color]


def suck(state: bool):
  """
  Set the suction cup on or off.

  Params
  ------
  state : bool
    The state that needs to be applied to the suction cup.
  """
  magician.set_endeffector_suctioncup(enable=state, on=state) # type: ignore


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
  str
    Command received from the server
  """
  try:
    response = requests.post(
      f"{SERVER_URL}/robot/color",
      json={"color": color},
      timeout=1
    )
    return response.json()["command"]
  except:
    return None


def send_status_to_pc(status: str):
  """
  Send robot status to the PC server.

  Params
  ------
  status : str
    Current robot status
  """
  try:
    requests.post(
      f"{SERVER_URL}/robot/status",
      json={"status": status},
      timeout=1
    )
  except:
    pass


### Main ###
def main():
  """
  When the robot detects a color, it sends it to the PC.
  The PC decides the destination and sends back a command.
  """

  POINT_COLOR_SENSOR = Point(0, 0, 0)

  WAREHOUSE_GREEN = Point(120, 0, 40)
  WAREHOUSE_RED = Point(0, 120, 40)
  WAREHOUSE_BLUE = Point(-120, 0, 40)

  while True:
    if get_color("green") == 1:
      color = "green"
    elif get_color("red") == 1:
      color = "red"
    elif get_color("blue") == 1:
      color = "blue"
    else:
      time.sleep(0.1)
      continue

    command = send_color_to_pc(color)
    if not command:
      continue

    send_status_to_pc("picking")

    move_to_point(POINT_COLOR_SENSOR)
    suck(True)
    time.sleep(0.3)

    if command == "MOVE_GREEN":
      move_to_point(WAREHOUSE_GREEN)
    elif command == "MOVE_RED":
      move_to_point(WAREHOUSE_RED)
    elif command == "MOVE_BLUE":
      move_to_point(WAREHOUSE_BLUE)

    suck(False)
    time.sleep(0.3)

    send_status_to_pc("idle")


#while True:
main()