FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV FLASK_APP flasky.py

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

CMD flask run --host 0.0.0.0 --port=80
