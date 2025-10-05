.DEFAULT_GOAL = bash
.ONESHELL:

DC_EXEC = docker compose exec -w /workspaces/timezone-service timezone-service

requirements: requirements/requirements.in
	docker compose run --rm -v ./:/home/service timezone-service uv pip compile -o requirements/requirements.txt requirements/requirements.in

test:
	$(DC_EXEC) /bin/bash -c "ptw ."

lint:
	$(DC_EXEC) /bin/bash -c "ruff check . && mypy ."

bash:
	$(DC_EXEC) /bin/bash

run-dev:
	$(DC_EXEC) fastapi dev --host 0.0.0.0 --port 8080 src/timezone_service

PORT=8081

build:
	docker compose build

run-production:
	docker run --rm -it -e PORT=8080 -p $(PORT):8080 timezone-service

smoketest:
	curl -sS http://localhost:$(PORT)/timezones > /dev/null && echo "SUCCESS" || echo "FAILURE"