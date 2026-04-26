# Communication between color sensor and infrared sensor

## Context

Topology

```txt
[robot 1] --- [pc 1 (flask server)]
                      |
[robot 2] --- [pc 2 (flask server)]
                      |
[robot 3] --- [pc 3 (flask server)]
```

Each robot is connected to its own local PC. Each PC runs an instance of the Flask server (the same server code is deployed on all three machines). These per-PC servers enable inter-robot communication by allowing servers to call each other over HTTP.

## Objective

When the color sensor endpoint is triggered on any PC, the local Flask server instance must notify the Flask server instance that hosts `robot_2` (PC 2). The `robot_2` process should wait for this notification and act only after receiving it.

## Required changes

- Extend the `color_sensor_event` endpoint so that, in addition to sending telemetry data to ThingsBoard, it also sends an HTTP request to `robot_2` notifying the color event.
- Modify the `robot_2` code so it waits for a confirmation/trigger from the server before executing logic that depends on the color event.
- Ensure that `robot_3` only detects and sends the color event to the server and does not perform additional local actions.
- Add in the .env file the ips of all the flask servers. So add these three lines:

  ```.env
  # existing code

  ROBOT_1_SERVER = "ip"
  ROBOT_2_SERVER = "ip"
  ROBOT_3_SERVER = "ip"
  ```

## Suggested implementation details

- Server endpoint: extend `color_sensor_event` to compose and send an HTTP request (e.g., POST) to the address of `robot_2` (host and port configurable via environment variables or a configuration file).
- Request payload to `robot_2`: include at minimum `ts` (timestamp), the source `robot_id`, and `color`.
- Robot 2: implement an HTTP listener (or a polling loop) that waits for the notification POST and responds with an acknowledgment; upon receipt, proceed with the intended processing.
- Robot 3: send the color event to the server and do not wait for responses from other robots.

## Considerations

- Error and timeout handling: the server should log errors when calling `robot_2` and consider retries or fallback behavior if necessary.
- Security: evaluate request authentication between server and robots (e.g., token-based authentication or an isolated network) if applicable.
- Testing: add end-to-end tests to verify that a color event triggers the notification to `robot_2` and that `robot_2` reacts only after receiving the notification.

## Next steps

1. Define the exact URL and payload for the call from `color_sensor_event` to `robot_2`.
2. Implement the call in the server and update `robot_3` if required.
3. Update `robot_2` to handle the notification and test the integration.

## Changes made

- Create two new endpoints in the flask server:
  - `/trigger`: sets a variable to indicate that the trigger has been received.
  - `/is_triggered`: if the trigger variable is set to true, returns true and makes the trigger variable false, else return false and do nothing.

- Add in the .env file the ips of all the flask servers. So add these three lines:

  ```.env
  # existing code

  ROBOT_1_SERVER = "ip"
  ROBOT_2_SERVER = "ip"
  ROBOT_3_SERVER = "ip"
  ```

- Modified the code of the robot 2 to poll the server every 0.5 seconds waiting for a trigger from the server before executing logic that depends on the color event.
