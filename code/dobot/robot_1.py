from DobotEDU import * # type: ignore
import time, datetime, requests

class Point():
  """Represents a point in the system of the robot"""

  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z

LINK: str = "http://127.0.0.10:8080/{}"
ROBOT_ID: int = 1

### Methods ###
def _log(msg: str):
  ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
  print(f"[{ts}] {msg}")

def move_to_point(p: Point, mode: int = 0):
  """Move the robot to the coordinate of the point with a mode"""

  print(f"[TELEMETRY] Moving to ({p.x}, {p.y}, {p.z}) | mode = {mode})")
  m_lite.set_ptpcmd(ptp_mode=mode, x=p.x, y=p.y, z=p.z, r = 0) # type: ignore



def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
  """Move the robot to the coordinate of the point  and the offset with a mode"""

  target_x = p.x + off_x
  target_y = p.y + off_y
  target_z = p.z + off_z

  print(f"[TELEMETRY] Moving to offset ({target_x}, {target_y}, {target_z}) | mode={mode}")
  m_lite.set_ptpcmd(ptp_mode=mode, x=target_x, y=target_y, z=target_z, r = 0) # type: ignore


def suck(state: bool):
  """Set the suction cup on or off"""

  status = "ON" if state else "OFF"
  print(f"[TELEMETRY] Suction cup {status}")
  m_lite.set_endeffector_suctioncup(enable=state, on=state) # type: ignore


def send_movement_executed(timeOfExecution: float):
  """
  Docstring for send_movement_executed
  """
  message = {
    "ts": str(time.time()),
    "robot_id": ROBOT_ID,
    "time": timeOfExecution
  }

  print(f"[send_movement_executed]: {message}")
  requests.post(LINK.format("robot/movement_executed"), json=message)


def main():
  print("[INFO] - Robot 1 started")

  collection_point = Point(167.73, 192.46, -28.79)
  conveyor_point = Point(247.6, -80.74, 42.53)

  safe_height = 30

  # Move above the collection point
  move_to_offpoint(collection_point, 0, 0, safe_height)

  while True:
    print("\n [INFO] - starting new cycle")

    # Move down to reach the block
    move_to_point(collection_point, mode=1)
    suck(True)

    move_to_point(conveyor_point)

    suck(False)

    move_to_offpoint(collection_point, 0, 0, safe_height)

    # 10. Wait before starting the next cycle
    print("[INFO] - Waiting 10 seconds before next cycle")
    time.sleep(3) # Put 3 for testing

main()






















