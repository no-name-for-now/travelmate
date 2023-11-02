DOCKER_IMAGE_NAME = "api"
DOCKER_IMAGE_TAG = "latest"

setup:
	@pip install --upgrade pip
	@pip install "poetry[all]"
	@$(MAKE) install
	@pre-commit install -c .precommit/.pre-commit-config.yaml
	@cp docker-compose/.example.env docker-compose/.env

install:
	@poetry lock
	@poetry install

docker-up:
	@docker compose up -d

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
