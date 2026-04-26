# Aggregator server

## Context

In the current configuration every robot has it's own server.
This is a quick sketch:

```txt
[robot 1] --- [pc 1 (flask server)]
                      |
[robot 2] --- [pc 2 (flask server)]
                      |
[robot 3] --- [pc 3 (flask server)]
```

The only method to communicate between servers is that every server has all the ip of the other servers.
This is inefficient and no one can have a full overview all in one place.

## Objective

The objective of this change is to create an aggregator server that aggregate all the logs of every server.
The server will have an endpoint that needs to be called from every local server when it logs something.

This will be the result:
![Data flow graph](/docs/_assets/dataFlowGraph.png)

## Required changes

- Create a `LoggerHelper` class that it will be useful to manage log. For example when the server needs to log something it calls the static method `LoggerHelper.log("message")` the method will: print the log to the console, send the log to the aggregator server and write the log message in to a log file.
- Create the aggregator server with the endpoint to log message.

## Next changes

A unified server is useful also to make send message between the local servers.
For example the fact that the robot 3 local server and robot 2 local server have to comunicate with the trigger is not efficient.
