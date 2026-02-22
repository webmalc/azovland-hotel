FROM python:3.13-slim-trixie


RUN apt-get update && apt-get install -y --no-install-recommends gettext libpq-dev binutils libproj-dev gdal-bin zlib1g-dev vim fish && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY uv.lock pyproject.toml ./
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"

COPY . .
