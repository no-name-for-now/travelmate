DOCKER_IMAGE_NAME = "api"
DOCKER_IMAGE_TAG = "latest"

setup:
	@pip install --upgrade pip
	@pip install "poetry[all]"
	@$(MAKE) install
	@pre-commit install -c .precommit/.pre-commit-config.yaml
	@cp .example.env .env

install:
	@poetry lock
	@poetry install

docker-up:
	@docker compose up -d

db-seed:
	python .local/scripts/seed.py

docker-down:
	@docker compose down

docker-build:
	@docker build --pull -t $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) -f Dockerfile .

docker-clean:
	@docker rmi -f $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
	@docker system prune -f --volumes

tilt-up:
	@tilt up

tilt-down:
	@tilt down

up: docker-up
down: docker-down

test-xmlrunner:
	@./manage.py test --no-input --keepdb

migrate:
	@./manage.py makemigrations
	@./manage.py migrate

run-local:
	@python -m gunicorn -c .configs/gunicorn.py tripagenda.asgi:app
