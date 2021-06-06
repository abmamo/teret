include .env
export $(shell sed 's/=.*//' .env)

help:
	@echo "list of available app commands"
	@echo
	@echo "available in a virtualenv"
	@echo "venv		- create virtual env."
	@echo "install		- install dependencies."
	@echo "routes      	- show all app routes."
	@echo "dev     	- run app in dev mode."
	@echo "prod        	- run app in prod mode."
	@echo "lint        	- lint app."
	@echo "test        	- test app."
	@echo "load-test       - load test app using locust."
	@echo "latest          - get latest version."
	@echo "release         - trigger deploy job."
	@echo
	@echo "to build docker containers"
	@echo "build-dev       - build dev app docker container."
	@echo "build-prod      - build prod app docker container."
	@echo "up-dev     	- run dev app docker container."
	@echo "up-prod     	- run prod app docker container."
	@echo "purge-dev     	- purge dev app docker container."
	@echo "purge-prod     	- purge prod app docker container."
	@echo "status-dev      - get dev app docker container status."
	@echo "status-prod     - get prod app docker container status."

# makefile args
# env variables
# app entrypoint
FLASK_APP := wsgi.py
# app env
FLASK_ENV := development
ENVIRONMENT := development
# default app port
DEFAULT_APP_PORT := 5000
# db uri
ifeq ($(DB_URI),)
APP_PORT := ${DEFAULT_APP_PORT}
endif
# docker container names
APP_CONTAINER_NAME_DEV := portfolio-dev
APP_CONTAINER_NAME_PROD := portfolio-prod

# virtualenv commands
install:
	@python3 -m pip install --upgrade pip && python3 -m pip install -r $(CURDIR)/requirements.txt
routes:
	@FLASK_APP=${FLASK_APP} FLASK_ENV=${FLASK_ENV} ENVIRONMENT=${ENVIRONMENT} PORT=${APP_PORT} python3 -m flask routes
dev:
	@echo "config: dev"
	@BG_ENABLED=${BG_ENABLED} FLASK_APP=${FLASK_APP} FLASK_ENV=${FLASK_ENV} ENVIRONMENT=${ENVIRONMENT} PORT=${APP_PORT} python3 -m flask run --host=0.0.0.0 --no-reload
prod:
	@echo "config: prod"
	@BG_ENABLED=${BG_DISABLED} FLASK_APP=${FLASK_APP} FLASK_ENV=production ENVIRONMENT=production PORT=${APP_PORT} python3 -m flask run --host=0.0.0.0 --no-reload
lint:
	@black src && black tests
	@PYTHONPATH=./src pylint src && pylint tests
test:
	@FLASK_APP=${FLASK_APP} FLASK_ENV=testing ENVIRONMENT=testing PORT=${APP_PORT} pytest --cov-report term-missing --cov=src tests -v && sleep 2.5 && rm -f .coverage*
load-test:
	make dev & locust -f $(CURDIR)/tests/test_load.py
latest:
	@git describe --abbrev=0
release:
	@git tag -a ${TAG} -m ${MESSAGE} && git push origin --tags

# docker commands
build-dev:
	@docker build -f ./dockerfiles/Dockerfile . -t ${APP_CONTAINER_NAME_DEV}:latest
build-prod:
	@docker build -f ./dockerfiles/Dockerfile.prod . -t ${APP_CONTAINER_NAME_PROD}:latest
up-dev: build-dev
	$(eval APP_CONTAINER_ID = $(shell (docker ps -aqf "name=${APP_CONTAINER_NAME_DEV}")))
	$(if $(strip $(APP_CONTAINER_ID)), \
		@echo "existing dev container found. please run make purge-dev",\
		@docker run -p 5000:5000 --name ${APP_CONTAINER_NAME_DEV} ${APP_CONTAINER_NAME_DEV}:latest)
	$(endif)
up-prod: build-prod
	$(eval APP_CONTAINER_ID = $(shell (docker ps -aqf "name=${APP_CONTAINER_NAME_PROD}")))
	$(if $(strip $(APP_CONTAINER_ID)), \
		@echo "existing prod container found. please run make purge-prod",\
		@echo "running app container..." && docker run -p ${APP_PORT}:${APP_PORT} --name ${APP_CONTAINER_NAME_PROD} ${APP_CONTAINER_NAME_PROD}:latest)
	$(endif)
purge-dev:
	$(eval APP_CONTAINER_ID = $(shell (docker ps -aqf "name=${APP_CONTAINER_NAME_DEV}")))
	$(if $(strip $(APP_CONTAINER_ID)), \
		@echo "purging dev app container..." && docker stop ${APP_CONTAINER_ID} && docker rm ${APP_CONTAINER_ID},\
		@echo "dev app container not running.")
	$(endif)
purge-prod:
	$(eval APP_CONTAINER_ID = $(shell (docker ps -aqf "name=${APP_CONTAINER_NAME_PROD}")))
	$(if $(strip $(APP_CONTAINER_ID)), \
		@echo "purging prod app container..." && docker stop ${APP_CONTAINER_ID} && docker rm ${APP_CONTAINER_ID},\
		@echo "prod app container not running.")
	$(endif)
status-dev:
	$(eval APP_CONTAINER_ID = $(shell (docker ps -aqf "name=${APP_CONTAINER_NAME_DEV}")))
	$(if $(strip $(APP_CONTAINER_ID)), \
		@echo "dev app container running",\
		@echo "dev app container not running.")
	$(endif)
status-prod:
	$(eval APP_CONTAINER_ID = $(shell (docker ps -aqf "name=${APP_CONTAINER_NAME_PROD}")))
	$(if $(strip $(APP_CONTAINER_ID)), \
		@echo "prod app container running",\
		@echo "prod app container not running.")
	$(endif)
