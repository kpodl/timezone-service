FROM python:3.13

ARG SERVICE_UID=${SERVICE_UID:-1000}
ARG HOME=/home/service
ENV PORT=8080

HEALTHCHECK --interval=1m --timeout=3s \
  CMD curl -f http://localhost:${PORT}/timezones || exit 1

RUN adduser --uid ${SERVICE_UID} --home ${HOME} service

RUN pip install uv

RUN mkdir /requirements
COPY requirements/requirements.txt /requirements/

RUN uv pip install --system -r /requirements/requirements.txt

USER service
WORKDIR ${HOME}

COPY data ${HOME}/data
COPY src ${HOME}/src

CMD exec fastapi run --host 0.0.0.0 --port ${PORT} src/timezone_service/
