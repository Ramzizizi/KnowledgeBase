#!/bin/bash

# SET LOGIC OF COMMANDS WORK (MAINLY DETERMINES HOW TO HANDLE ERRORS)
set -Eeuo pipefail

# ABSOLUTE PATH TO WORK DIR
BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd -P)"
APP_DIR="${BASE_DIR}/src"
export PYTHONPATH="${APP_DIR}"

# FUNC FOR GET ENVS FROM ".env" FILE
if [[ -f "${BASE_DIR}/.env" ]]; then
  echo "[entrypoint] Loading .env ..."
  source "${BASE_DIR}/.env"
  set +a
fi


# ACTIVATE VENV
source .venv/bin/activate

# RUN ALEMBIC MIGRATIONS
echo "[entrypoint] Applying DB migrations..."
alembic upgrade head

# LOAD ENVS PARAMS FROM ".env" FOR UVICORN
APP_IMPORT="${APP_IMPORT:-knowledge_base.main:app}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
WORKERS="${WORKERS:-4}"

# START APP
cd "${APP_DIR}"
echo "[entrypoint] Starting Uvicorn: ${APP_IMPORT} on ${HOST}:${PORT} (workers=${WORKERS})"
uvicorn "${APP_IMPORT}" --host "${HOST}" --port "${PORT}" --workers "${WORKERS}"