from DobotEDU import * # type: ignore
import time, requests, datetime, atexit

# Set the version of the wheel
magicbox.set_device_withl(enable=True, version=0) # type: ignore
magicbox.set_infrared_sensor(port=2, enable=True, version=1) # type: ignore
magician.motion_params(100, 100) # type: ignore
magician.jump_params(200, 30) # zlimit, height # type: ignore

class Point():
  """Represents a point in the system of the robot"""

  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z

  def plus(self, x, y, z):
    return Point(x=self.x + x, y=self.y + y, z=self.z + z)

#https://www.dobot-robots.com/service/download-center

LINK: str = "http://10.33.77.2:8080/{}"
ROBOT_ID: int = 2

def _log(msg: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{ts}] {msg}")

### Methods ###
def move_to_point(p: Point, mode: int = 0):
  """Move the robot to the coordinate of the point with a mode"""

  _log(f"[TELEMETRY] Moving to ({p.x}, {p.y}, {p.z}) | mode = {mode})")
  magician.ptp(mode=mode, x=p.x, y=p.y, z=p.z, r = 0) # type: ignore


def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
  """Move the robot to the coordinate of the point  and the offset with a mode"""

  target = Point(x=p.x + off_x, y=p.y + off_y, z=p.z + off_z)

  _log(f"[TELEMETRY] Moving to offset ({target.x}, {target.y}, {target.z}) | mode={mode}")
  move_to_point(target, mode=mode)


def suck(state: bool):
  """Set the suction cup on or off"""

  status = "ON" if state else "OFF"
  _log(f"[TELEMETRY] Suction cup {status}")
  magician.set_endeffector_suctioncup(enable = state, on = state) # type: ignore

def get_ir_sensor_status() -> bool:
  return True if magicbox.get_infrared_sensor(port=2)["status"] == 1 else False # type: ignore


def set_conv_speed(speed: int):
  magicbox.set_converyor(index=magicbox.STP1,enable=True,speed=speed) # type: ignore

# Method to send data to the local server
"""
def test_connectivity() -> tuple[bool, int]:
  try:
    res = requests.get(LINK.format("status"), timeout=3)
    return res.status_code == 200, res.status_code
  except Exception as e:
    _log(f"[ERROR] {e=}")
    return False, 404
"""

def send_ir_event(t = time.time()):
  message = {
    "ts": str(t),
    "robot_id": ROBOT_ID,
    "status": "success"
  }

  _log(f"[send_ir_event]: {message}")
  requests.post(url=LINK.format("robot/infrared_sensor_event"), json=message)


def send_ir_error():
  message = {
    "ts": str(time.time() * 1000),
    "robot_id": ROBOT_ID,
    "status": "error"
  }

  _log(f"[send_ir_error]: {message}")
  requests.post(url=LINK.format("robot/infrared_sensor_event"), json=message)


def send_movement_executed(timeOfExecution: float):
  message = {
    "ts": str(time.time() * 1000),
    "robot_id": ROBOT_ID,
    "time": timeOfExecution
  }

  _log(f"[send_movement_executed]: {message}")
  requests.post(url=LINK.format("robot/movement_executed"), json=message)


def wait_for_is_triggered(poll_interval: float = 1.0):
  """
  Poll the server endpoint `/is_triggered` until it returns True.

  The server is expected to respond with JSON containing the key
  `message` set to a boolean (True/False). This function will block
  until that value becomes True. It logs attempts and sleeps
  `poll_interval` seconds between requests.
  """
  url = LINK.format("robot2/can_drop")

  _log(f"[INFO] - Polling {url} every {poll_interval}s for trigger")

  while True:
    try:
      resp = requests.get(url, timeout=3)
      if resp.status_code == 200:
        try:
          data = resp.json()
        except Exception:
          _log(f"[WARN] Invalid JSON from {url}: {resp.text}")
          data = None

        triggered = None
        if isinstance(data, dict):
          triggered = data.get("message")
        else:
          # fallback: accept bare boolean responses
          triggered = data

        if triggered is True:
          _log("[INFO] Server returned triggered=True, continuing")
          return True
        else:
          _log("[INFO] Server not ready yet (trigger=False). Waiting...")
      else:
        _log(f"[WARN] is_triggered returned status {resp.status_code}")
    except Exception as e:
      _log(f"[WARN] Error contacting is_triggered endpoint: {e}")

    time.sleep(poll_interval)


def send_block_dropped():
  link = LINK.format("robot2/block_dropped")
  ret = requests.post(url=link)


def reset():
  _log("[INFO] Reset method")
  set_conv_speed(0)
  suck(False)

def test():
  dropPointRed: Point = Point(65.94, 251.38, -91.17)
  dropPointGreen: Point = Point(-80.08, 271.15, -91.08)
  dropPointBlue: Point = Point(-18.76, 273.4, -90.88)
  dropPointNone: Point = Point(-39.6, -237.95, 97.63)

  move_to_point(dropPointRed)
  time.sleep(5)
  move_to_point(dropPointGreen)
  time.sleep(5)
  move_to_point(dropPointBlue)



def detect_color() -> str:
  l = LINK.format("/robot2/detect_color")
  res = requests.get(l)
  color = res.json()["message"]
  _log(f"[detect_color] Color detected = {color}")
  return color


def main():
  _log("[INFO] - Enter main method")

  """
  status, code = test_connectivity()
  if not status or code != 200:
    _log("[ERROR] Can't connect to the server")
    _log(f"[ERROR] {status=}")
    _log(f"[ERROR] {code=}")
    return
  """

  # Variables
  CONV_SPEED: int = 100

  timeOfExecution: float = 0 # seconds
  timeStart: float ; timeEnd: float
  lastCheck: float = time.time()

  # Define the collection point and the drop point
  # If the drop point is not perfectly alined the block will move farther way every iteration
  # so adjust the x coordinate of the drop point to be more precise
  collectionPoint: Point = Point(211.62, -132.87, -35.37)
  sensorPoint: Point = Point(145.85, -192.13, -16.92)
  dropPointRed: Point = Point(65.94, 251.38, -91.17)
  dropPointGreen: Point = Point(-80.08, 271.15, -91.08)
  dropPointBlue: Point = Point(-18.76, 273.4, -90.88)
  dropPointNone: Point = Point(-39.6, -237.95, 97.63)

  try:
    # Go above the collection point
    _log("[INFO] - Move above the collection point")
    move_to_offpoint(collectionPoint, 0, 0, 5)

    # Get up to speed  the conveyor
    _log("[INFO] - Take the conveyor up to speed")
    set_conv_speed(CONV_SPEED) # Comment this line is in debug

    # Reset lastCheck before starting the cycle
    lastCheck = time.time()

    _log("[INFO] - Enter main cycle")

    # In documentation there is a complete documentation of this cycle
    # If you change the cycle update the documentation
    while True:
      sensor = get_ir_sensor_status()
      if sensor:
        timeStart = time.time()
        suck(True) # Set this to False for debugging

        # Get the block on the fly
        move_to_offpoint(collectionPoint, 0, 0, 0, 1)
        move_to_offpoint(collectionPoint, 0, 0, 20, 1)

        # Go to the drop point
        move_to_point(sensorPoint)

        # When the robot reach the drop point calculates the time of the movement
        timeEnd = time.time()

        timeOfExecution = timeEnd - timeStart
        _log(f"[INFO] - Cycle executed in {timeOfExecution} seconds")

        # Send the time of execution to the server
        send_movement_executed(timeOfExecution)

        color = detect_color()

        # Poll the server until it allows the robot to continue
        wait_for_is_triggered()

        # Move to the dropPoint
        move_to_offpoint(sensorPoint, 0, 0, 50)

        if color == "red":
          move_to_point(dropPointRed)
        elif color == "green":
          move_to_point(dropPointGreen)
        elif color == "blue":
          move_to_point(dropPointBlue)
        else:
          move_to_point(dropPointNone)

        suck(False)

        # Return to the collection point
        move_to_offpoint(collectionPoint, 0, 0, 5)

        send_block_dropped()

        # Send the last time the robot put down a block
        send_ir_event()

        lastCheck = time.time()

      # If the sensor doesn't get triggered, check how much time has passed between now and the last block.
      # If the time is less than 20, send a infrared sensor error to the local server
      else:
        # Check how long the sensor is idle
        # If more than 20 seconds, send a infrared_sensor_error
        t = time.time()
        if lastCheck is not None and t - lastCheck > 20:
          _log("[INFO] - No block has passed")
          send_ir_error()
          lastCheck = time.time()
  except Exception as e:
    _log(f"[ERROR] - {e}")
  finally:
    reset()

# Register the function reset to be called on program exit
# The function reset will be called when the program closes normally or with an unhandled exception
atexit.register(reset)

main()
