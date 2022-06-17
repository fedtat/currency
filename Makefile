SHELL := /bin/bash

manage_py := docker exec -it backend python app/manage.py

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

run:
	$(manage_py) runserver 0:8001

uwsgi:
	uwsgi --chdir /home/highlight/PycharmProjects/currency/app/ --http 127.0.0.1:8000 --wsgi-file settings/wsgi.py --master --processes 4 --threads 2 --max-requests 1000 --http-timeout 10

run-dev: migrate \
	run

worker:
	cd app && celery -A settings worker -l info --autoscale 1,10

beat:
	cd app && celery -A settings beat -l info

flake8:
	docker exec -it backend flake8 app/

pytest:
	docker exec -it backend pytest ./app/tests --cov=app --cov-report html -vv && coverage report --fail-under=67
