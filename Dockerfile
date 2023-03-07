FROM python:3.10-slim

WORKDIR /code
COPY  requirements.txt .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r requirements.txt
COPY manage.py .
COPY todolist .
COPY core .

CMD python manage.py runserver 0.0.0.0:8000