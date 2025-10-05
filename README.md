# Timezone Service

This repository contains a dockerized service to retrieve timezones from a shapefile.

## Build

Use `make build` to use `docker compose` to build the service.

Alternatively, you can use `docker` directly:
```bash
$ docker build -t timezone-service .
```

## Run

Use `make run-production` to start a production server or `make run-dev` to start a development server in an already running `docker compose` environment.