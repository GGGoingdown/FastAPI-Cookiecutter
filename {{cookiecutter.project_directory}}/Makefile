### Compose shortcuts
up:
	echo "Service up"
	docker-compose --env-file ./env/.dev.env  up -d
	docker-compose --env-file ./env/.dev.env logs -f app
down:
	echo "Service down"
	docker-compose --env-file ./env/.dev.env  down
test:
	echo "Service testing"
	docker-compose --env-file ./env/.test.env  build --build-arg ENVIRONMENT=TEST
	docker-compose --env-file ./env/.test.env  up -d
	docker exec -it app pytest
	docker-compose --env-file ./env/.test.env  down

build:
	echo "Build images"
	docker-compose --env-file ./env/.dev.env  build --build-arg ENVIRONMENT=DEV

build_no_cache:
	echo "Build images no cache"
	docker-compose --env-file ./env/.dev.env  build --build-arg ENVIRONMENT=DEV --no-cache

create_doc:
	echo "Create documents"
	docker-compose --env-file ./env/.test.env  up -d
	docker exec -it app python doc_generator.py --remove-old True
	widdershins docs/api-docs-*.json -o README.md --language_tabs 'python:Python'
	docker-compose --env-file ./env/.dev.env  down
	sudo chmod -R 777 docs/

create_env:
	echo "Create development environment"
	cp ./env/.cookiecutter.env ./env/.dev.env
	sed -i 's/ENVIRONMENT="DEV"/ENVIRONMENT="DEV"/g' ./env/.dev.env
	echo "Create testing environment"
	cp ./env/.cookiecutter.env ./env/.test.env
	sed -i 's/ENVIRONMENT="DEV"/ENVIRONMENT="TEST"/g' ./env/.test.env

	chmod -R +x ./env
	echo "Remove cookiecutter.env"
	rm -f ./env/.cookiecutter.env
