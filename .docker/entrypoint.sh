#!/bin/sh
set -e

chown -R appuser:appgroup /app/static /app/media

exec gosu appuser "$@"
