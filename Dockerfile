FROM python:3.11.5-bullseye
RUN apt update -y \
    && apt upgrade -y \
    && apt autoremove -y \
    && apt install firefox-esr -y

COPY . /app

RUN python -m pip install poetry && cd /app && poetry build && pip install dist/*.whl

ENTRYPOINT ["/bin/sh", "-c"]
