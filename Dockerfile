# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

RUN apk add --no-cache build-base libffi-dev

RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
WORKDIR /app

CMD ["python3", "-u", "main.py"]

FROM builder as dev-envs

RUN apk update && apk add git

RUN addgroup -S docker && adduser -S --shell /bin/bash --ingroup docker vscode
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
