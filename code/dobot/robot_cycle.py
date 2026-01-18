from DobotEDU import * # type: ignore
import time, requests

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


BASE_LINK: str = "http://127.0.0.5:8080/robot/"
ROBOT_ID: int = 2

### Methods =^.^= ###
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

def send_ir_event():
    """
    Docstring for send_ir_event
    """
    message = {
        "ts": str(time.time()),
        "robot_id": ROBOT_ID,
        "status": "success"
    }

    requests.post(url=BASE_LINK + "/infrared_sensor_event", json=message)


def send_ir_error():
    """
    Docstring for send_ir_error
    """
    message = {
        "ts": str(time.time()),
        "robot_id": ROBOT_ID,
        "status": "error"
    }

    requests.post(url=BASE_LINK + "/infrared_sensor_event", json=message)


def send_movement_executed(timeOfExecution: float):
    """
    Docstring for send_movement_executed
    """
    message = {
        "ts": str(time.time()),
        "robot_id": ROBOT_ID,
        "time": timeOfExecution
    }

    requests.post(url=BASE_LINK + "/movement_executed", json=message)



### Method to send data to the local server ###
# TODO add method to send data to the local server, there are in ./code/test/robot_bp_test.py
# The commented line that start with "#$", they have to be uncommented if you have to send message to the server

def reset():
    print("[INFO] - Reset method")
    set_conv_speed(0)
    suck(False)


def main():
    print("[INFO] - Enter main method")
    # Variables
    CONV_SPEED: int = 100

    timeOfExecution: float = 0 # seconds
    timeStart: float ; timeEnd: float
    #$lastCheck: float

    # Define the collection point and the drop point
    # If the drop point is not perfectly alined the block will move farther way every iteration
    # so adjust the x coordinate of the drop point to be more precise
    collectionPoint: Point = Point(129.51, -199.44, 20.71)

    try:
        # Go above the collection point
        print("[INFO] - Move above the collection point")
        move_to_offpoint(collectionPoint, 0, 0, 5)

        # Get up to speed  the conveyor
        print("[INFO] - Take the conveyor up to speed")
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
                #$lastCheck = time.time()
                # Send a infrared_sensor_event to the server
                #$send_ir_event()

                timeStart = time.time()
                suck(True)

                # Get the block on the fly
                move_to_offpoint(collectionPoint, 0, 0, 0, 1) # MOV 1
                move_to_offpoint(collectionPoint, 0, 0, 20, 1) # MOV 2

                # Go to the drop point
                move_to_offpoint(collectionPoint, 80, 0, 10, 1) # MOV 3
                move_to_offpoint(collectionPoint, 80, 300, 10, 1) # MOV 4
                move_to_offpoint(collectionPoint, 0, 300, 5, 1) # MOV 5

                suck(False)

                # Return to the collection point
                move_to_offpoint(collectionPoint, 80, 300, 10, 1) # MOV 6
                move_to_offpoint(collectionPoint, 80, 0, 10, 1) # MOV 7
                move_to_offpoint(collectionPoint, 0, 0, 5, 1) # MOV 8
                timeEnd = time.time()

                timeOfExecution = timeEnd - timeStart
                print(f"[INFO] - Cycle executed in {timeOfExecution} seconds")

                # Send the time of execution to the server
                #$send_movement_executed(timeOfExecution)

            # If the sensor doesn't get triggered, check how much time has passed between now and the last block.
            # If the time is less than 20, send a infrared sensor error to the local server
            #$else:
                # Check how long the sensor is idle
                # If more than 30 seconds, send a infrared_sensor_error
                #$if time.time() - lastCheck > 20:
                    #$print("[INFO] - No block has passed")
                    #$send_ir_error()  
    except Exception as e:
        print(f"[ERROR] - {e}")
    finally:
        set_conv_speed(0)
        suck(False)


main()
