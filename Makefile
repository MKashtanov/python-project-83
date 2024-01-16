PORT ?= 8000

build:
	./build.sh

lint:
	poetry run flake8 page_analyzer

install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 1 -b 0.0.0.0:$(PORT) page_analyzer:app