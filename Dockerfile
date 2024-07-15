FROM python:3.12-slim AS requirements
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-slim
RUN apt update && \
    apt upgrade -y && \
    mkdir -p /srv/app && \
    useradd -d /srv/app app && \
    chown app:app /srv/app

WORKDIR /srv/app
COPY --chown=app:app --from=requirements /tmp/requirements.txt /srv/app/requirements.txt
COPY --chown=app:app ./firefly_report_bot /srv/app/firefly_report_bot
RUN python3 -m venv venv && \
    venv/bin/pip install --no-cache-dir --upgrade pip && \
    venv/bin/pip install --no-cache-dir -r /srv/app/requirements.txt

CMD ["venv/bin/python", "-m", "firefly_report_bot"]
