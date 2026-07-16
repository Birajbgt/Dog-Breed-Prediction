#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_LOG="$ROOT_DIR/backend.log"
FRONTEND_LOG="$ROOT_DIR/frontend.log"

port_in_use() {
  ss -ltn | awk '{print $4}' | grep -qE '(^|:)(8000|3000)$'
}

if ss -ltn | awk '{print $4}' | grep -qE '(^|:)(8000)$'; then
  echo "Backend already running on http://127.0.0.1:8000"
else
  cd "$ROOT_DIR"
  source .venv/bin/activate
  nohup uvicorn api:app --host 0.0.0.0 --port 8000 >"$BACKEND_LOG" 2>&1 &
  echo "Backend running at http://127.0.0.1:8000"
fi

if ss -ltn | awk '{print $4}' | grep -qE '(^|:)(3000)$'; then
  echo "Frontend already running on http://127.0.0.1:3000"
else
  cd "$ROOT_DIR/frontend"
  nohup npm run dev -- --host 0.0.0.0 --port 3000 >"$FRONTEND_LOG" 2>&1 &
  echo "Frontend running at http://127.0.0.1:3000"
fi

echo "Logs:"
echo "  $BACKEND_LOG"
echo "  $FRONTEND_LOG"
