from DobotEDU import * # type: ignore
import time, datetime, requests

magician.motion_params(100, 100) # vel, acc # type: ignore

class Point():
  """Represents a point in the system of the robot"""

  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z

LINK: str = "http://10.33.77.10:8080/{}"
ROBOT_ID: int = 1

### Methods ###
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

### Method to send data to the local server ###

def test_connectivity():
  try:
    res = requests.get(LINK.format("status"), timeout=3)
    return res.status_code == 200, res.status_code
  except Exception as e:
    _log(f"[ERROR] {e=}")
    return False, 404

def send_movement_executed(timeOfExecution: float):
  """
  Docstring for send_movement_executed
  """
  message = {
    "ts": str(time.time()),
    "robot_id": ROBOT_ID,
    "time": timeOfExecution
  }

  _log(f"[send_movement_executed]: {message}")
  requests.post(LINK.format("robot/movement_executed"), json=message)


def wait_for_is_triggered(poll_interval: float = 1.0):
  """
  Poll the server endpoint `/is_triggered` until it returns True.

  The server is expected to respond with JSON containing the key
  `message` set to a boolean (True/False). This function will block
  until that value becomes True. It logs attempts and sleeps
  `poll_interval` seconds between requests.
  """
  url = LINK.format("robot1/can_collect")

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


def main():
  print("[INFO] - Robot 1 started")

  status, code = test_connectivity()
  if not status or code != 200:
    _log("[ERROR] Can't connect to the server")
    _log(f"[ERROR] {status=}")
    _log(f"[ERROR] {code=}")
    return

  collection_point = Point(225.58, 0, -40.97)
  conveyor_point = Point(236.79, 136.17, 26.16)

  safe_height = 20

  _log("[INFO] Showing the collection point")
  # Move above the collection point to show it
  move_to_offpoint(collection_point, 0, 0, safe_height)
  time.sleep(5)

  while True:
    _log("\n [INFO] - starting new cycle")

    # TODO measure the movement_executed

    # Move down to reach the block
    move_to_point(collection_point)
    suck(True)

    move_to_point(conveyor_point)

    suck(False)

    move_to_offpoint(conveyor_point, 0, 0, 30, 1)

    # Wait for server to allow next cycle
    wait_for_is_triggered()

main()
