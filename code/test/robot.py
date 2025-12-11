import time, requests, datetime

class Message():
  """ Create a message """
  link: str = "http://127.0.0.10:8080/robot/"
  robot_id: int = 2

  @classmethod
  def create(cls, timeOfExecution = None):
    if timeOfExecution == None:
      return {
        "ts": str(time.time()),
        "robot_id": cls.robot_id,
      }
    else:
      return {
        "ts": str(time.time()),
        "robot_id": cls.robot_id,
        "time": timeOfExecution
      }

### Method to send data to the local server ###
def send_ir_event():
  """
  Docstring for send_ir_event
  """
  requests.post(
    url=Message.link + "/infrared_sensor_event", 
    json=Message.create()
  )


def send_ir_error():
  """
  Send a message with timestamp and robot id to
  """
  requests.post(
    url=Message.link + "/infrared_sensor_error", 
    json=Message.create()
  )


def send_movement_executed(timeOfExecution: float):
  """
  Send the movement_executed event to the server.
  """
  req = requests.post(
    url=Message.link + "movement_executed",
    json=Message.create(timeOfExecution=timeOfExecution)
  )

  print(f"{req=}")


#send_ir_error()
#send_ir_event()
send_movement_executed(5)
time.sleep(3)
send_movement_executed(5)
time.sleep(3)
send_movement_executed(7)
time.sleep(3)
send_movement_executed(3)
