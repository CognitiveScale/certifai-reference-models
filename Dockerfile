FROM python:3.6-slim

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD . /model_server

WORKDIR /model_server

CMD [ "python", "-m", "model_server" ]