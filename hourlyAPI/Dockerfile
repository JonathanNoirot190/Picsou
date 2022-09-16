FROM python:3.9-slim

RUN mkdir -p /hourly/logs
RUN mkdir -p /hourly/prices
WORKDIR /hourly
ADD requirements.txt /hourly
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ADD instance instance
ADD hourly hourly
ADD config config
ADD classic-hourly.py classic-hourly.py

EXPOSE 5000
ENTRYPOINT ["gunicorn", "--config", "config/gunicorn_config.py", "hourly.wsgi:app"]
