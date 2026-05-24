#!/usr/bin/env bash
set -euo pipefail

: "${BOT_TOKEN:?BOT_TOKEN is required}"
: "${APP_PUBLIC_BASE_URL:?APP_PUBLIC_BASE_URL is required}"
: "${BOT_WEBHOOK_SECRET:?BOT_WEBHOOK_SECRET is required}"

WEBHOOK_URL="${APP_PUBLIC_BASE_URL%/}/telegram/webhook"

curl -fsS -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
  -d "url=${WEBHOOK_URL}" \
  -d "secret_token=${BOT_WEBHOOK_SECRET}"
