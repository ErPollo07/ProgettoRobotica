from typing import Optional
import time
import requests
import random
import math
import argparse
from datetime import datetime

LINK: str = "http://127.0.0.10:8080/{}"
ROBOT_ID: int = 2

class Point:
    """Represents a point in the system of the robot (simulator)."""

    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

# Simulated state
_current_position = Point(0.0, 0.0, 0.0)
_conv_speed = 0
_last_sensor_time = 0.0

def _log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{ts}] {msg}")


def move_to_point(p: Point, mode: int = 0):
    """Simulate movement to an absolute point with a printed estimate and sleep."""
    global _current_position
    start = _current_position
    target = p
    dist = math.sqrt((target.x - start.x) ** 2 + (target.y - start.y) ** 2 + (target.z - start.z) ** 2)
    duration = max(0.5, dist / 150.0)
    _log(f"[SIM] Moving from ({start.x:.1f}, {start.y:.1f}, {start.z:.1f}) to ({target.x:.1f}, {target.y:.1f}, {target.z:.1f}) | mode={mode} | est {duration:.2f}s")
    time.sleep(duration)
    _current_position = Point(target.x, target.y, target.z)
    _log(f"[SIM] Arrived at ({_current_position.x:.1f}, {_current_position.y:.1f}, {_current_position.z:.1f})")


def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
    """Simulate movement to a point + offset."""
    target = Point(p.x + off_x, p.y + off_y, p.z + off_z)
    _log(f"[SIM] Moving to offset point ({target.x:.1f}, {target.y:.1f}, {target.z:.1f}) | mode={mode}")
    move_to_point(target, mode=mode)


def suck(state: bool):
    """Simulate turning the suction cup on or off."""
    status = "ON" if state else "OFF"
    _log(f"[SIM] Suction cup {status}")
    time.sleep(0.4)


def get_ir_sensor_status() -> bool:
    """Simulate an infrared sensor occasionally triggering.

    To keep the output readable we avoid firing more often than every 1.5s.
    """
    global _last_sensor_time
    now = time.time()
    if now - _last_sensor_time < 1.5:
        return False
    triggered = random.random() < 0.15
    if triggered:
        _last_sensor_time = now
        _log("[SIM] Infrared sensor TRIGGERED (simulated)")
    return triggered


def set_conv_speed(speed: int):
    """Simulate setting conveyor speed."""
    global _conv_speed
    _conv_speed = speed
    _log(f"[SIM] Conveyor speed set to {speed}")


### Method to send data to the local server ###

def test_connectivity() -> tuple[bool, int]:
    try:
        res = requests.get(LINK.format("status"), timeout=3)
        return res.status_code == 200, res.status_code
    except Exception as e:
        _log(f"[ERROR] {e=}")
        return False, 404



def send_ir_event(t: float | None = None):
    if t is None:
        t = time.time()
    message = {
        "ts": str(t),
        "robot_id": ROBOT_ID,
        "status": "success"
    }
    _log(f"[send_ir_event]: {message}")
    try:
        resp = requests.post(url=LINK.format("robot/infrared_sensor_event"), json=message, timeout=3)
        _log(f"[HTTP] infrared_sensor_event status: {resp.status_code}")
    except Exception as e:
        _log(f"[WARN] Could not send infrared_sensor_event: {e}")


def send_ir_error():
    message = {
        "ts": str(time.time()),
        "robot_id": ROBOT_ID,
        "status": "error"
    }
    _log(f"[send_ir_error]: {message}")
    try:
        resp = requests.post(url=LINK.format("robot/infrared_sensor_event"), json=message, timeout=3)
        _log(f"[HTTP] infrared_sensor_event status: {resp.status_code}")
    except Exception as e:
        _log(f"[WARN] Could not send infrared_sensor_event: {e}")


def send_movement_executed(timeOfExecution: float):
    message = {
        "ts": str(time.time()),
        "robot_id": ROBOT_ID,
        "time": timeOfExecution
    }
    _log(f"[send_movement_executed]: {message}")
    try:
        resp = requests.post(url=LINK.format("robot/movement_executed"), json=message, timeout=3)
        _log(f"[HTTP] movement_executed status: {resp.status_code}")
    except Exception as e:
        _log(f"[WARN] Could not send movement_executed: {e}")


def wait_for_is_triggered(poll_interval: float = 1.0):
    """Poll the server's `/is_triggered` endpoint until it returns True."""
    url = LINK.format("is_triggered")

    _log(f"[SIM] Polling {url} every {poll_interval}s for trigger (simulator)")

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
                    triggered = data

                if triggered is True:
                    _log("[SIM] Server returned triggered=True, continuing")
                    return True
                else:
                    _log("[SIM] Server not ready yet (trigger=False). Waiting...")
            else:
                _log(f"[WARN] is_triggered returned status {resp.status_code}")
        except Exception as e:
            _log(f"[WARN] Error contacting is_triggered endpoint: {e}")
        time.sleep(poll_interval)


def reset():
    _log("[INFO] - Reset method (simulator)")
    set_conv_speed(0)
    suck(False)


def main(cycles: Optional[int] = 3):
    _log("[INFO] - Enter main method (simulator)")

    # Check connectivity with the local server
    status, code = test_connectivity()

    if not status or code != 200:
        _log("[ERROR] Can't connect to the server")
        _log(f"[ERROR] {status=}")
        _log(f"[ERROR] {code=}")
        return

    CONV_SPEED = 100
    timeOfExecution = 0.0
    lastCheck = time.time()

    # Define points (same as original)
    collectionPoint = Point(230, 100, 60)
    sensorPoint = Point(230, 0, 60)
    dropPoint = Point(230, -100, 60)

    try:
        _log("[INFO] - Move above the collection point")
        move_to_offpoint(collectionPoint, 0, 0, 5)

        _log("[INFO] - Take the conveyor up to speed")
        set_conv_speed(CONV_SPEED)

        _log("[INFO] - Enter main cycle")
        cycles_done = 0
        while True:
            if cycles is not None and cycles_done >= cycles:
                _log("[INFO] - Reached configured cycles, exiting main loop")
                break

            sensor = get_ir_sensor_status()
            if sensor:
                lastCheck = time.time()

                timeStart = time.time()
                suck(True)

                move_to_offpoint(collectionPoint, 0, 0, 0, 1)
                move_to_offpoint(collectionPoint, 0, 0, 20, 1)

                move_to_point(sensorPoint)

                timeEnd = time.time()
                timeOfExecution = timeEnd - timeStart
                _log(f"[INFO] - Cycle executed in {timeOfExecution:.2f} seconds")

                send_ir_event(lastCheck)

                wait_for_is_triggered()

                move_to_offpoint(dropPoint, 0, 0, 5)

                suck(False)

                move_to_offpoint(collectionPoint, 0, 0, 5)

                send_movement_executed(timeOfExecution)
                cycles_done += 1
            else:
                t = time.time()
                if lastCheck is not None and t - lastCheck > 20:
                    _log("[INFO] - No block has passed (simulated)")
                    send_ir_error()
                    lastCheck = time.time()

            time.sleep(0.5)
    except KeyboardInterrupt:
        _log("[INFO] - Interrupted by user (simulator)")
    except Exception as e:
        _log(f"[ERROR] - {e}")
    finally:
        set_conv_speed(0)
        suck(False)

    _log("[INFO] - Simulator exiting")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulated PC runner for robot_2")
    parser.add_argument("--cycles", type=int, default=3, help="Number of simulated pick cycles to run (default 3). Use 0 for infinite.")
    args = parser.parse_args()
    run_cycles = None if args.cycles == 0 else args.cycles
    main(run_cycles)
