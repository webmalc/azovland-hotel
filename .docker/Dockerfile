FROM python:3.13-slim-trixie

RUN apt-get update && apt-get install -y --no-install-recommends \
  gettext libpq-dev binutils libproj-dev gdal-bin zlib1g-dev vim fish gosu \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appgroup && useradd -r -m -g appgroup appuser

WORKDIR /app
RUN chown appuser:appgroup /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --chown=appuser:appgroup uv.lock pyproject.toml ./
RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=appuser:appgroup . .
COPY .docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
