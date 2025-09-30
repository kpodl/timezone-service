dependencies:
	docker compose run --rm -v ./:/home/service timezone-service uv pip compile -o requirements/requirements.txt requirements/requirements.in