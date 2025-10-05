DC_EXEC = docker compose exec -w /workspaces/timezone-service timezone-service

requirements: requirements/requirements.in
	docker compose run --rm -v ./:/home/service timezone-service uv pip compile -o requirements/requirements.txt requirements/requirements.in

test:
	$(DC_EXEC) /bin/bash -c "ptw ."

lint:
	$(DC_EXEC) /bin/bash -c "ruff check . && mypy ."

bash:
	$(DC_EXEC) /bin/bash