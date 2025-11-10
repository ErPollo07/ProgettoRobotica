from DobotEDU import *


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
      - 1: go strait to the destination point
  """
  magician.ptp(mode, p.x + off_x, p.y + off_y, p.z + off_z, 0) # type: ignore


def suck(state: bool):
  """
  Set the suction cup on or off.

  Params
  ------
  state : bool
    The state that needs to be applied to the suction cup.
  """
  magician.set_endeffector_suctioncup(enable=state, on=state) # type: ignore
