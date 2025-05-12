#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Default fallback values
: "${HOST:=127.0.0.1}"
: "${PORT:=8000}"
: "${APP_MODULE:=app.main:app}"

# Handle commands
if [[ "$1" == "--scheduler" ]]; then
  shift
  echo "Running scheduler with args: $@"
  python -m app.services.scheduler "$@"
else
  echo "Starting FastAPI app at $HOST:$PORT from $APP_MODULE..."
  uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT"
fi
