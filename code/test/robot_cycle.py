from DobotEDU import * # type: ignore


# Set the version of the wheel
magicbox.set_device_withl(enable=True, version=0) # type: ignore
magicbox.set_infrared_sensor(port=2, enable=True, version=1) # type: ignore
magician.motion_params(100, 100) # type: ignore

class Point():
  """Represents a point in the system of the robot"""
  
  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z

### Methods ###
def get_sensor_status() -> int:
  """
  Gets the infrared sensor status

  Returns
  ------
  int
    0 if the sensor doesn't detect anything
    1 if the sensor detect anything
  """
  return magicbox.get_infrared_sensor(port=2)["status"] # type: ignore

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


def set_conv_speed(speed: int):
  """
  Set the conveyor speed.

  Params
  ------
  speed : int
    The speed to set to the conveyor.
  """
  magicbox.set_converyor(index=magicbox.STP1,enable=True,speed=speed) # type: ignore


def suck(state: bool):
  """
  Set the suction cup on or off.

  Params
  ------
  state : bool
    The state that needs to be applied to the suction cup.
  """
  magician.set_endeffector_suctioncup(enable=state, on=state) # type: ignore


"""
# Un comment these lines and comment all the line below to stop the conveyor and the suctioncup
set_conv_speed(0)
suck(False)
"""

# Variables
CONV_SPEED: int = 100

# Define the collection point and the drop point
# If the drop point is not perfectly alined the block will move farther way every iteration
# so adjust the x coordinate of the drop point to be more precise
collectionPoint: Point = Point(136.0, -201.0, 14.0)
dropPoint: Point = Point(collectionPoint.x - 3, collectionPoint.y + 150, collectionPoint.z + 5)

try:
  # Go above the collection point
  print("[INFO] - Move above the collection point")
  move_to_offpoint(collectionPoint, 0, 0, 4)

  # Get up to speed  the conveyor
  print("[INFO] - Take the conveyor app to speed")
  set_conv_speed(CONV_SPEED)

  # Take the block while the conveyor is moving]
  # When the infrared sensor detect something the robot:
  # - start the suctioncup
  # - go to the collectionPoint
  # - take the block 
  # - go to dropPoint
  # - release the block
  # - return above the collectionPoint
  print("[INFO] - Enter main cycle")
  while True:
    sensor = get_sensor_status()
    if sensor == 1:
      suck(True)
      move_to_offpoint(collectionPoint, 0, -7, 0, 1)
      move_to_offpoint(collectionPoint, 0, -7, 20, 1)
      move_to_point(dropPoint, 1)
      suck(False)
      move_to_offpoint(collectionPoint, 0, 0, 4, 1)
except Exception as e:
  print(f"[ERROR] - {e}")
finally:
  set_conv_speed(0)
  suck(False)
