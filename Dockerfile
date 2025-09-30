FROM python:3.13

ARG SERVICE_UID=${SERVICE_UID:-1000}
ARG HOME=/home/service

RUN adduser --uid ${SERVICE_UID} --home ${HOME} service

RUN pip install uv

RUN mkdir /requirements
COPY requirements/requirements.txt /requirements/

RUN uv pip install --system -r /requirements/requirements.txt

USER service
WORKDIR ${HOME}
