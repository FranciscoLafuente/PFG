FROM python:3.7.1

RUN apt-get update -y && \
    pip install --upgrade pip && \
    apt-get install -y python-pip python-dev

ENV FLASK_APP "flasky.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD flask run --host 0.0.0.0
