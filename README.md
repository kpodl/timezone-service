# Timezone Service

This repository contains a dockerized service to retrieve timezones from a shapefile.

## Build

Use `make build` to use `docker compose` to build the service.

Alternatively, you can use `docker` directly:
```bash
$ docker build -t timezone-service .
```

## Development

The following `make` targets are provided:

- `bash`: Open a shell on a running containe.
- `test`: Continuously run tests on file changes.
- `lint`: Run linting and type checking.

Checkout the `Makefile` for other targets.

## Server

### Production
Use `make run-production` to start a production server.


### Development
When **not** using VSCode's devcontainers run `docker compose up` to start a dev server on port `8080`.

For using devcontainers you should include `.devcontainer/docker-compose.yml` by setting up a `.env` file:
```.env
DOCKER_COMPOSE="docker-compose.yml:.devcontainer/docker-compose.yml"
```
