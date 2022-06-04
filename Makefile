SHELL := /bin/bash

manage_py := python app/manage.py

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

run:
	$(manage_py) runserver

uwsgi:
	uwsgi --chdir app/ --http 127.0.0.1:8000 --wsgi-file settings/wsgi.py --master --processes 4 --threads 2 --max-requests 1000 --http-timeout 10

run-dev: migrate \
	run

worker:
	cd app && celery -A settings worker -l info --autoscale 1,10

beat:
	cd app && celery -A settings beat -l info

pytest:
	pytest ./app/tests --cov=app --cov-report html
