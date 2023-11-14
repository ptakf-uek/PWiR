# syntax = docker/dockerfile:1.5.2

FROM python:3.11-bookworm as backend-dev

WORKDIR /PWiR
COPY backend .

# Where to store apt libs
ARG APT_LIB_DIR=/var/lib/apt
# Where to store apt cache
ARG APT_CACHE_DIR=/var/cache/apt

RUN --mount=type=cache,target=$APT_CACHE_DIR,sharing=locked \
    --mount=type=cache,target=$APT_LIB_DIR,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache && \
    apt-get update && apt install tree

RUN tree
COPY ci/requirements/backend-dev-requirements.txt requirements.txt

ARG PIP_CACHE_DIR=/var/cache/pip
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    pip install -r requirements.txt && rm requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
