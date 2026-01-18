# version: Python3
from DobotEDU import *
import requests, time


magician.set_color_sensor(port=2, enable=True, version=1)


class Point():
    """Represents a point in the system of the robot"""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


### Configuration ###
SERVER_URL = "http://192.168.1.100:8080"


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


def get_color_sensor():
    """Return the raw color sensor data"""
    return magicbox.get_color_sensor()


def get_color(color: str):
    """Return 1 if the specified color is detected"""
    return get_color_sensor()[color]


def suck(state: bool):
    """
    Set the suction cup on or off.

    Params
    ------
    state : bool
        The state that needs to be applied to the suction cup.
    """
    magician.set_endeffector_suctioncup(enable=state, on=state) # type: ignore


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
        requests.post(f"{SERVER_URL}/robot/color", json=message)
        return True, None
    except Exception as e:
        return False, str(e)

### Main ###
def main():
    """
    When the robot detects a color, it sends it to the PC.
    The PC decides the destination and sends back a command.
    """

    # TODO Add a counter for how many blocks there are every warehouse (make a Warehouse class)

    COLLECTION_POINT = Point(0, 0, 0)
    IDLE_POINT = Point(100,100,100) # TODO define an idle point (will be near the collection point)

    WAREHOUSE_GREEN = Point(120, 0, 40)
    WAREHOUSE_RED = Point(0, 120, 40)
    WAREHOUSE_BLUE = Point(-120, 0, 40)

    # Declaring variables
    color: str ; point: Point = COLLECTION_POINT; pick: bool = False

    move_to_point(point)

    while True:
        color_detected = get_color_sensor()

        # Check if any of the color is detected
        if color_detected["green"] == 1:
            color = "green"
            point = WAREHOUSE_GREEN
        elif color_detected["red"] == 1:
            color = "red"
            point = WAREHOUSE_RED
        elif color_detected["blue"] == 1:
            color = "blue"
            point = WAREHOUSE_BLUE
        else:
            pick = False
            continue

        status, error = send_color_to_pc(color)

        # collect the block
        move_to_point(COLLECTION_POINT)
        suck(True)

        # Put the block in the correct warehouse
        move_to_point(point)
        suck(False)

        move_to_point(IDLE_POINT)


#while True:
main()
