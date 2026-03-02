from DobotEDU import *
import time

class Point():
    """Represents a point in the system of the robot"""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z




#==================================
#=========== METHODS ==============
#==================================

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

