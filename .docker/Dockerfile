FROM python:3.13-slim-trixie

RUN apt-get update && apt-get install -y --no-install-recommends \
  gettext libpq-dev binutils libproj-dev gdal-bin zlib1g-dev vim fish \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./uv.lock pyproject.toml ./
RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN uv run manage.py collectstatic --no-input --clear

ENTRYPOINT [".venv/bin/gunicorn", "az.wsgi:application", "--bind", "unix:/var/run/gunicorn/gunicorn.sock"]
