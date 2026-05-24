# Telegram Bot Platform

Reusable scaffold for a Telegram bot platform with a Python backend, Telegram webhook support, PostgreSQL persistence, and a Telegram Mini App frontend.

## Bill of Software

| Component | Technology | Purpose |
|---|---|---|
| Backend API | Python, FastAPI | Handles health checks, webhook processing, and Mini App API requests |
| Bot logic | Python | Parses Telegram updates and routes bot commands |
| Data layer | SQLAlchemy, Alembic | Manages persistence and schema migrations |
| Database | PostgreSQL | Stores users, chats, sessions, update logs, file metadata, and audit data |
| Frontend | Vite, TypeScript | Provides the Telegram Mini App user interface |
| Reverse proxy | Apache2 | Serves frontend assets and routes traffic to the backend |
| Service manager | systemd | Runs the backend as a managed Linux service |
| Webhook registration | Bash + curl | Registers Telegram webhooks against the Bot API |
| Container image | Docker | Packages the backend for deployment |

## Components and Purpose

### Backend API
The FastAPI backend exposes health endpoints, Telegram webhook endpoints, and authenticated Mini App APIs.

### Bot Logic
The bot layer isolates Telegram-specific parsing, command dispatching, and response creation from HTTP transport concerns.

### Persistence Layer
The repository and model structure are designed to keep database access explicit, typed, and migration-driven.

### File Storage
Storage abstractions keep file handling separate from application logic and make local or S3-compatible storage swappable.

### Frontend Mini App
The frontend provides the in-Telegram UI that communicates with the backend through authenticated API calls.

### Deployment Assets
Apache, systemd, and webhook scripts provide the baseline for Linux deployment and Telegram integration.

## Project Structure

- `backend/` – FastAPI backend, bot logic, persistence, storage, and tests
- `frontend/` – Vite + TypeScript Mini App frontend
- `deploy/` – Apache, systemd, and webhook helper assets
- `docs/` – requirements, architecture, security, testing, and runbook documentation

## Installation

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+

### Backend setup

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

### Frontend setup

```bash
cd frontend
npm install
```

### Environment configuration

Copy the example environment file from `deploy/` and fill in values:

```bash
cp deploy/.env.example .env
```

Required values include:

- `BOT_TOKEN`
- `BOT_WEBHOOK_SECRET`
- `DATABASE_URL`
- `APP_PUBLIC_BASE_URL`
- `FRONTEND_PUBLIC_URL`

## Running the software

### Start the backend

```bash
cd backend
. .venv/bin/activate
uvicorn app.main:app --reload
```

### Start the frontend

```bash
cd frontend
npm run dev
```

### Start PostgreSQL locally

If you want a local database for development, use Docker Compose from the `deploy/` directory:

```bash
docker compose -f deploy/docker-compose.yml up -d db
```

### Health checks

- `GET /health` – liveness
- `GET /ready` – dependency readiness

## Developing functionality

### Backend workflow

1. Add or update code under `backend/app/`.
2. Keep Telegram logic inside `backend/app/bot/`.
3. Keep HTTP routes inside `backend/app/api/`.
4. Keep persistence logic inside `backend/app/repositories/`.
5. Add tests under `backend/app/tests/`.

### Frontend workflow

1. Add UI code under `frontend/src/`.
2. Keep Telegram Web Apps integration isolated in frontend modules.
3. Validate builds with `npm run build`.

### Recommended checks

```bash
# Backend syntax check
python -m compileall backend/app

# Frontend build
cd frontend
npm run build
```


## Docker

### Build the backend image

From the repository root:

```bash
docker build -t telegram-bot-platform-backend -f backend/Dockerfile backend
```

### Run the backend container

```bash
docker run --rm -p 8000:8000   --env-file .env   telegram-bot-platform-backend
```

### Use with Docker Compose

To start PostgreSQL for local development:

```bash
docker compose -f deploy/docker-compose.yml up -d db
```

You can then run the backend locally against the database or adapt the compose file to include the backend service.


## Telegram Mini Apps

This platform includes a Telegram Mini App frontend that runs inside the Telegram client.

### How it is used

1. The user opens the bot in Telegram.
2. The bot provides a path to the Mini App.
3. Telegram loads the frontend in an in-app web view.
4. The frontend reads Telegram-provided context such as user identity and `initData`.
5. The frontend sends `initData` to the backend for server-side validation.
6. The backend validates the request and returns authenticated session data.
7. The Mini App renders the user interface and can call authenticated backend endpoints.

### Expected flow in this repository

- The frontend lives under `frontend/`.
- The backend Mini App API lives under `backend/app/api/routes_miniapp.py`.
- Authentication validation logic belongs in `backend/app/services/miniapp_auth_service.py`.
- Telegram-specific data should always be validated on the server before being trusted.

### Development notes

- Use Telegram Web Apps SDK in the frontend.
- Do not trust frontend user IDs without backend validation.
- Keep Mini App API calls behind authenticated backend endpoints.
- Use `/api/me` to fetch the current authenticated user/session state.

### How users launch the Mini App

Users can open the Mini App from within Telegram in one of these ways:

- Tap the Mini App button that the bot exposes in the chat interface.
- Use the bot menu entry if the bot is configured with a web app shortcut.
- Open the bot and choose the Mini App from the bot’s interface when prompted.

When launched, Telegram opens the frontend inside an in-app browser and passes Telegram context to the Mini App. The frontend should read `initData`, send it to the backend, and wait for server validation before showing authenticated content.

## Deployment notes

- Use `deploy/apache/telegram-bot.conf` for Apache reverse proxy configuration.
- Use `deploy/systemd/telegram-bot.service` for the backend service.
- Use `deploy/scripts/register_webhook.sh` to register the Telegram webhook.

## Documentation

See `docs/` for the product requirements, architecture, security controls, testing requirements, and operational runbook.
