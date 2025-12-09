# Thingsboard setup

This file contains a set by set guide on how to set up the thingsboard service on your local machine.

If this guide don't work see [thingsboard installation guide](https://thingsboard.io/docs/user-guide/install/installation-options/).

## Before installation

Make sure to have these software installed:

- [Docker desktop](http://docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

## Steps

### 1. Clone the thingsboard repository

The first step is to clone the [thingsboard repository](https://github.com/thingsboard/thingsboard).

```bash
git clone https://github.com/thingsboard/thingsboard.git
```

### 2. Change the docker-compose.yml file

Enter the directory `./thingsboard/docker`.

This is the command needed:

```bash
cd thingsboard/docker
```

Overwrite the docker-compose.yml file with these line:

```yml
services:
  postgres:
    restart: always
    image: "postgres:16"
    ports:
      - "5432"
    environment:
      POSTGRES_DB: thingsboard
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data
  thingsboard-ce:
    restart: always
    image: "thingsboard/tb-node:4.2.1"
    ports:
      - "8080:8080"
      - "7070:7070"
      - "1883:1883"
      - "8883:8883"
      - "5683-5688:5683-5688/udp"
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "10"
    environment:
      TB_SERVICE_ID: tb-ce-node
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/thingsboard
    depends_on:
      - postgres

volumes:
  postgres-data:
    name: tb-postgres-data
    driver: local
```

### 3. Initialize database schema & system assets

Run the following command in the `./thingsboard/docker` directory.

```bash
docker compose run --rm -e INSTALL_TB=true -e LOAD_DEMO=true thingsboard-ce
```

## Start and the thingsboard server

Now all the set up is done, so you can run the server with this command:

```bash
docker compose up -d
```

To stop the server:

```bash
docker compose down
```
