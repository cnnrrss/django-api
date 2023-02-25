COMMIT := $(shell git log --pretty=format:'%h' -n 1)
DATE := $(shell date -u +.%Y%m%d.%H%M%S)
VERSION := $(COMMIT)$(DATE)


PKG_NAME=dashboard


migrations:
	python3 $(PKG_NAME)/manage.py makemigrations

migrate:
	python3 $(PKG_NAME)/manage.py migrate
