#!/bin/sh
set -e

: "${DEBUG:=false}"

if [ $# -eq 0 ] || [ "${1#-}" != "$1" ]; then
  if [ "$DEBUG" = "true" ]; then
    echo "Running in DEBUG mode with auto-reload"
    exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
  else
    echo "Running in PRODUCTION mode"
  exec uvicorn src.main:app --host 0.0.0.0 --port 8000
  fi
fi

exec "$@"
