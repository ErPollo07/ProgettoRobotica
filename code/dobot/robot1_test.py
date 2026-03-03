from DobotEDU import *
import time

class Point():
    """Represents a point in the system of the robot"""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z




# ==================================
# =========== METHODS ==============
# ==================================

def move_to_point(p: Point, mdoe: int = 0):
    """Move the robot to the coordinate of the point with a mode"""

    print(f"[TELEMETRY] Moving to ({p.x}, {p.y}, {p.z}) | mode = {mode})")
    m_lite.set_ptpcmd(ptp_mode=mode, x=p.x, y=p.x, z=p.z, r = 0)



def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0): 
    """Move the robot to the coordinate of the point  and the offset with a mode"""

    target_x = p.x + off_x
    target_y = p.y + off_y
    target_z = p.z + off_z

    print(f"[TELEMETRY] Moving to offset ({target_x}, {target_y}, {target_z}) | mode={mode}")
    m_lite.set_ptpcmd(ptp_mode=mode, x=target_x, y=target_y, z=target_z, r = 0)



def suck(state: bool):
    """Set the suction cup on or off"""

    status = "ON" if state else "OFF"
    print(f"[TELEMETRY] Suction cup {status}")
    m_lite.set_endeffector_suctioncup(enable = state, on = state)


# ==============================
# =========== MAIN =============
# ==============================

def main():
    print("[INFO] - Robot 1 started")

    collection_point = Point(0, 0, 0)
    conveyor_point = Point(0, 0, 0) 

    safe_height = 50

    while true:
        print("\n [INFO] - starting new cycle")

        # 1. Move above the collection point
        move_to_offpoint(collection_point, 0, 0, safe_height, mode=0)

        # 2. Move down to reach the block
        move_to_point(collection_point, mode=1)

        # 3. Activate suction cup to grab the block
        suck(True)
        time.sleep(1)

        # 4. Lift the block to a safe height
        move_to_offpoint(collection_point, 0, 0, safe_height, mode=1)

        # 5. Move above the conveyor belt
        move_to_offpoint(conveyor_point, 0, 0, safe_height, mode=0)

        # 6. Move down to the conveyor position
        move_to_point(conveyor_point, mode=1)

        # 7. Deactivate suction cup to release the block
        suck(False)
        time.sleep(1)

        # 8. Lift back to safe height above conveyor
        move_to_offpoint(conveyor_point, 0, 0, safe_height, mode=1)

        # 9. Return above the collection point
        move_to_offpoint(collection_point, 0, 0, safe_height, mode=0)

        # 10. Wait before starting the next cycle
        print("[INFO] - Waiting 10 seconds before next cycle")
        time.sleep(10)


main()
