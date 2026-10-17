#!/usr/bin/env bash
# Run the interactive notebook viewer locally: chat backend + gallery dev server.
#
#   scripts/dev-local.sh           PORT=3000 (gallery), chat backend on 127.0.0.1:8077
#
# The backend is started first and polled on /health; the gallery dev server starts
# once it is ready. Killing this script (or Ctrl-C) kills both.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

PORT="${PORT:-3000}"
CHAT_PORT="${CHAT_PORT:-8077}"
HEALTH_URL="http://127.0.0.1:${CHAT_PORT}/health"

backend_pid=""
web_pid=""

cleanup() {
  trap - INT TERM EXIT
  for pid in "${web_pid:-}" "${backend_pid:-}"; do
    [ -n "$pid" ] || continue
    pkill -P "$pid" 2>/dev/null || true # npm/uv intermediate processes
    kill "$pid" 2>/dev/null || true
  done
  wait 2>/dev/null || true
}
trap cleanup INT TERM EXIT

# All three extras are named explicitly: `uv run` prunes any extra not listed, and
# the kernel subprocess needs PySpark/pandas (notebooks-spark) for the Spark topics
# while the notebook scripts (nbformat, nbclient, ipykernel) need `notebooks`.
uv run --extra notebooks --extra notebooks-spark --extra interactive \
  uvicorn backend.main:app --host 127.0.0.1 --port "${CHAT_PORT}" &
backend_pid=$!

printf 'dev-local: waiting for chat backend on %s ...\n' "$HEALTH_URL"
ready=0
for _ in $(seq 1 60); do
  if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then ready=1; break; fi
  if ! kill -0 "$backend_pid" 2>/dev/null; then
    echo 'dev-local: backend exited before becoming ready' >&2
    exit 1
  fi
  sleep 0.5
done
if [ "$ready" -ne 1 ]; then
  echo "dev-local: backend did not become ready within 30s" >&2
  exit 1
fi

npm run dev -- --port "${PORT}" &
web_pid=$!

printf 'dev-local: gallery on http://localhost:%s, chat on %s (Ctrl-C to stop both)\n' "$PORT" "$HEALTH_URL"
wait "$web_pid"
