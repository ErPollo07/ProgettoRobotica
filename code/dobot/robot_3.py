# version: Python3
from DobotEDU import * # type: ignore
import time, requests


magician.set_color_sensor(port=2, enable=True, version=1) # type: ignore

### Configuration ###
LINK: str = "http://127.0.0.10:8080/robot/{}"

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
    requests.post(LINK.format("color_sensor_event"), json=message)
    return True, None
  except Exception as e:
    return False, str(e)


def compute_color(values):
  if values == (1, 0, 0):
    return "red",
  elif values == (0, 1, 0):
    return "green",
  elif values == (0, 0, 1):
    return "blue",
  else:
    return None

### Main ###
def main():
  """
  When the robot detects a color, it sends it to the PC.
  The PC decides the destination and sends back a command.
  """

  # TODO Add a counter for how many blocks there are every warehouse (make a Warehouse class)

  # Declaring variables
  color: str | None

  while True:
    color_detected = get_color_sensor()

    print(color_detected)

    # Check if any of the color is detected
    color = compute_color(tuple(color_detected.values()))

    if color != None:
      # status, error = send_color_to_pc(color)

      send_color_to_pc(color)

      color = None


while True:
  main()
