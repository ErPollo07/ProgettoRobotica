# Database

## What database is used

For this project has been chosen the thingsboard service.

### What is Thingsboard

ThingsBoard is an open-source IoT platform that provides telemetry ingestion, data processing, device management, and visualization capabilities.  
For this project, ThingsBoard has been selected as the primary data storage and monitoring solution due to:

- native support for time-series data,
- integration through standard protocols (HTTP/MQTT),
- built-in dashboards for real-time monitoring,
- the ability to manage multiple devices independently.

## Dataflow description

Every robot send data to a local server on the network created using python.

So this is the flow of the data of the robot:

```txt
  *------*       *--------------*       *-------------*
  | Data | ----> | Local server | ----> | Thingsboard |
  *------*       *--------------*       *-------------*
```

## Telemetry requirements

Each robot produces different type of telemetry.
However, all robot measure the duration of each movement.
This is require to keep track of mechanical wear that can produce degradation over time and slow or stop the production.

### Robot specific telemetry

#### Robot 1

- Movement duration: time needed to perform his action

#### Robot 2

- Infrared sensor event: when a block has been detected passing in front of the infrared sensor.
- Infrared sensor error: if no block passes within a predefined interval, an error event is logged to indicate a possible flow interruption

#### Robot 3

- Color sensor event: log the color of the block arrived at destination
