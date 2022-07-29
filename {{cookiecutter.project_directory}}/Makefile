### Compose shortcuts
up:
	echo "Service up"
	docker-compose --env-file ./env/.dev.env  up -d
down:
	echo "Service down"
	docker-compose --env-file ./env/.dev.env  down
test:
	echo "Service testing"
	docker-compose --env-file ./env/.test.env  up -d
	docker exec -it app pytest
	docker-compose --env-file ./env/.test.env  down

build:
	echo "Build images"
	docker-compose --env-file ./env/.dev.env  build --build-arg ENVIRONMENT=DEV

build_no_cache:
	echo "Build images no cache"
	docker-compose --env-file ./env/.dev.env  build --build-arg ENVIRONMENT=DEV --no-cache
