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


LINK: str = f"http://127.0.0.5:8080/robot/{0}"
ROBOT_ID: int = 2

### Methods ###
def move_to_point(p: Point, mode: int = 0):
  """Move the robot to the coordinate of the point with a mode"""

  print(f"[TELEMETRY] Moving to ({p.x}, {p.y}, {p.z}) | mode = {mode})")
  magician.ptp(ptp_mode=mode, x=p.x, y=p.y, z=p.z, r = 0) # type: ignore


def move_to_offpoint(p: Point, off_x: float, off_y: float, off_z: float, mode: int = 0):
  """Move the robot to the coordinate of the point  and the offset with a mode"""

  target_x = p.x + off_x
  target_y = p.y + off_y
  target_z = p.z + off_z

  print(f"[TELEMETRY] Moving to offset ({target_x}, {target_y}, {target_z}) | mode={mode}")
  magician.ptp(ptp_mode=mode, x=target_x, y=target_y, z=target_z, r = 0) # type: ignore


def suck(state: bool):
  """Set the suction cup on or off"""

  status = "ON" if state else "OFF"
  print(f"[TELEMETRY] Suction cup {status}")
  magician.set_endeffector_suctioncup(enable = state, on = state) # type: ignore


def set_conv_speed(speed: int):
  """
  Set the conveyor speed.

  Params
  ------
  speed : int
    The speed to set to the conveyor.
  """
  magicbox.set_converyor(index=magicbox.STP1,enable=True,speed=speed) # type: ignore


def get_sensor_status() -> bool:
  """
  Gets the infrared sensor status
  """
  return True if magicbox.get_infrared_sensor(port=2)["status"] == 1 else False # type: ignore


def send_ir_event():
  """
  Docstring for send_ir_event
  """
  message = {
    "ts": str(time.time()),
    "robot_id": ROBOT_ID,
    "status": "success"
  }

  requests.post(url=LINK.format("/infrared_sensor_event"), json=message)


def send_ir_error():
  """
  Docstring for send_ir_error
  """
  message = {
    "ts": str(time.time()),
    "robot_id": ROBOT_ID,
    "status": "error"
  }

  requests.post(url=LINK.format("/infrared_sensor_event"), json=message)


def send_movement_executed(timeOfExecution: float):
  """
  Docstring for send_movement_executed
  """
  message = {
    "ts": str(time.time()),
    "robot_id": ROBOT_ID,
    "time": timeOfExecution
  }

  requests.post(url=LINK.format("/movement_executed"), json=message)


### Method to send data to the local server ###
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

        # Take the block while the conveyor is moving
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
            if sensor:
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
                # If more than 20 seconds, send a infrared_sensor_error
                #$if time.time() - lastCheck > 20:
                    #$print("[INFO] - No block has passed")
                    #$send_ir_error()
    except Exception as e:
        print(f"[ERROR] - {e}")
    finally:
        set_conv_speed(0)
        suck(False)


main()
