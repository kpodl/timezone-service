.DEFAULT_GOAL = bash
.ONESHELL:

DC_EXEC = docker compose exec timezone-service

containers-running:
	docker compose up -d --no-recreate

requirements: requirements/requirements.in
	docker compose run --rm -v ./:/home/service timezone-service uv pip compile -o requirements/requirements.txt requirements/requirements.in

test: containers-running
	$(DC_EXEC) /bin/bash -c "ptw ."

lint: containers-running
	$(DC_EXEC) /bin/bash -c "ruff check . && mypy ."

bash: containers-running
	$(DC_EXEC) /bin/bash

run-dev: containers-running
	$(DC_EXEC) fastapi dev --host 0.0.0.0 --port 8080 src/timezone_service

PORT=8081

build:
	docker compose build

run-production:
	docker run --rm -it -e PORT=8080 -p $(PORT):8080 timezone-service

smoketest:
	curl -sS http://localhost:$(PORT)/timezones > /dev/null && echo "SUCCESS" || echo "FAILURE"