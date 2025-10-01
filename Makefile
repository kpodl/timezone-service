dependencies:
	docker compose run --rm -v ./:/home/service timezone-service uv pip compile -o requirements/requirements.txt requirements/requirements.in

bash:
	docker compose exec timezone-service /bin/bash -c "cd /workspaces/timezone-service; /bin/bash"