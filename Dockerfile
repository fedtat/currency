FROM python:3.9

WORKDIR /code/build

RUN apt update -y && apt install python3.9-dev -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH /code/build/app

# CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]

CMD ["uwsgi", "--http", ":8000", "--chdir", "/code/build/app", "--wsgi-file", "settings/wsgi.py", \
    "--processes", "4", "--threads", "2", "--max-requests", "1000", "--http-timeout", "10"]
