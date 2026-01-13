# version: Python3
from DobotEDU import *


magician.set_color_sensor(port=2, enable=True, version=1)


class Point():
  """Represents a point in the system of the robot"""
  
  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z


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
  return magicbox.get_color_sensor()


def get_color(color: str):
  get_color_sensor()[color]


def suck(state: bool):
  """
  Set the suction cup on or off.

  Params
  ------
  state : bool
    The state that needs to be applied to the suction cup.
  """
  magician.set_endeffector_suctioncup(enable=state, on=state) # type: ignore

def main():
  """
  When the robot sees a difference beetwen the color detected a moment before and the current color,
  it will take the block on the color sensor and move it to the specific warehouse.
  """
  POINT_COLOR_SENSOR = Point(0, 0, 0)
  # print(magician.get_color_sensor())
  while True:
    colors = get_color_sensor()
    print(colors)
    if get_color("green") == 1:
      point_1 = Point(0, 0, 0)
      move_to_point(point_1)
      move_to_point(POINT_COLOR_SENSOR)
    elif get_color("red") == 1:
      point_1 = Point(0, 0, 0)
      move_to_point(point_1)
      move_to_point(POINT_COLOR_SENSOR)
    elif get_color("blue") == 1:
      point_1 = Point(0, 0, 0)
      move_to_point(point_1)
      move_to_point(POINT_COLOR_SENSOR)


#while True:
main()
