from typing import Optional
import time
import requests
import math
import argparse
from datetime import datetime

LINK: str = "http://127.0.0.10:8080/{}"
ROBOT_ID: int = 1

class Point:
    """Represents a point in the system of the robot (simulator)."""

    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


# Simulated state
_current_position = Point(0.0, 0.0, 0.0)
_conv_speed = 0


def _log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{ts}] {msg}")


def move_to_point(p: Point, mode: int = 0):
    """Simulate movement to an absolute point with an estimate and sleep."""
    global _current_position
    start = _current_position
    target = p
    dist = math.sqrt((target.x - start.x) ** 2 + (target.y - start.y) ** 2 + (target.z - start.z) ** 2)
    duration = max(0.3, dist / 150.0)
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
    time.sleep(0.35)


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


def send_movement_executed(timeOfExecution: float):
    message = {
        "ts": str(time.time()),
        "robot_id": ROBOT_ID,
        "time": timeOfExecution,
    }
    _log(f"[send_movement_executed]: {message}")
    try:
        resp = requests.post(url=LINK.format("robot/movement_executed"), json=message, timeout=3)
        _log(f"[HTTP] movement_executed status: {resp.status_code}")
    except Exception as e:
        _log(f"[WARN] Could not send movement_executed: {e}")


def wait_for_is_triggered(poll_interval: float = 1.0):
    """Poll the server endpoint `/is_triggered` until it returns True.

    This simulates the blocking wait used by `robot_1.py`.
    """
    url = LINK.format("robot_1/is_triggered")

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
    _log("[INFO] - Enter main method (simulator for robot_1)")

    status, code = test_connectivity()
    if not status or code != 200:
        _log("[ERROR] Can't connect to the server")
        _log(f"[ERROR] {status=}")
        _log(f"[ERROR] {code=}")
        return

    # Points mirroring robot_1.py
    collection_point = Point(-18, -222, 105)
    conveyor_point = Point(182, -172, 100)
    idle_point = Point(93, -222, 105)

    safe_height = 20

    try:
        _log("[INFO] Showing the collection point (simulator)")
        move_to_offpoint(collection_point, 0, 0, safe_height)
        time.sleep(1)

        cycles_done = 0
        while True:
            if cycles is not None and cycles_done >= cycles:
                _log("[INFO] - Reached configured cycles, exiting main loop")
                break

            _log("\n[INFO] - starting new cycle (simulator)")

            # Move down to reach the block
            t0 = time.time()
            move_to_point(collection_point)
            suck(True)

            # Move to conveyor and drop
            move_to_point(conveyor_point)
            suck(False)

            # Move to idle
            move_to_point(idle_point)

            t1 = time.time()
            elapsed = t1 - t0
            _log(f"[INFO] - Cycle executed in {elapsed:.2f} seconds (simulator)")
            send_movement_executed(elapsed)

            # Wait for server to allow next cycle
            wait_for_is_triggered()

            cycles_done += 1
            time.sleep(0.4)

    except KeyboardInterrupt:
        _log("[INFO] - Interrupted by user (simulator)")
    except Exception as e:
        _log(f"[ERROR] - {e}")
    finally:
        reset()

    _log("[INFO] - Simulator exiting")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulated PC runner for robot_1")
    parser.add_argument("--cycles", type=int, default=3, help="Number of simulated pick cycles to run (default 3). Use 0 for infinite.")
    args = parser.parse_args()
    run_cycles = None if args.cycles == 0 else args.cycles
    main(run_cycles)
