<!-- docs/PROJECT_BRIEF.md -->

# Project Brief: General Telegram Bot Platform

## Related Documents

| Document | Purpose |
|---|---|
| `PROJECT_BRIEF.md` | Project context and goals |
| `PRD.md` | Product requirements |
| `ARCHITECTURE.md` | Technical architecture |
| `RUNBOOK.md` | Operations and deployment |
| `CODING_STANDARDS.md` | Coding conventions |
| `TESTING_REQUIREMENTS.md` | Testing expectations |
| `SECURITY_REQUIREMENTS.md` | Security controls |

## 1. Purpose

Build a reusable Telegram bot platform with:

- Python backend
- Telegram Bot API webhook integration
- Telegram Mini App frontend
- PostgreSQL persistence
- File storage abstraction
- Secure configuration
- Production-oriented Linux deployment

The platform should be a clean foundation for future Telegram bot products, not a one-off bot implementation.

## 2. Target Platform

The application targets Telegram users interacting through:

- Bot commands
- Bot messages
- Buttons
- Deep links
- Telegram Mini Apps

Primary integration method:

- Telegram Bot API over HTTPS webhooks

Mini Apps are treated as the main rich UI layer for Telegram users.

## 3. Minimal Architecture

### Required Components

| Component | Purpose |
|---|---|
| Telegram account | Used to create and manage the bot through BotFather |
| Telegram bot | Public Telegram-facing application identity |
| API server | Public HTTPS endpoint for Telegram webhook requests |
| Backend service | Python application handling bot logic and APIs |
| Telegram Mini App | Web UI opened inside Telegram clients |
| Web server | Hosts frontend assets and reverse-proxies backend traffic |
| PostgreSQL database | Stores users, sessions, updates, app state, and metadata |
| File storage | Stores uploaded or generated files |
| Git repository | Source control and AI-agent context |

### Optional Components

| Component | Purpose |
|---|---|
| Secrets store | Secure credential management |
| Admin console | Operational and management UI |
| Centralized logging | Aggregated runtime logs |
| Monitoring | Health, metrics, alerts, and availability checks |

## 4. Preferred Technology Stack

### Backend

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x or SQLModel
- Alembic
- Uvicorn or Gunicorn with Uvicorn workers

### Frontend

- Node.js LTS
- TypeScript
- HTML5
- CSS3
- JavaScript
- Vite
- Telegram Web Apps SDK

### Database

- PostgreSQL

### Infrastructure

Preferred defaults:

- Ubuntu 22.04
- AWS
- GitHub
- Apache2
- Let’s Encrypt
- Local storage for development
- S3-compatible storage for production

## 5. Runtime Flow

### Bot Webhook Flow

1. User sends a command, message, or button action to the Telegram bot.
2. Telegram sends an HTTPS webhook request to the backend.
3. Reverse proxy forwards the request to the Python API service.
4. Backend validates the request.
5. Dispatcher routes the update to the correct handler.
6. Business logic reads or writes database state.
7. Backend sends a response through the Telegram Bot API.

### Mini App Flow

1. User opens the Mini App from Telegram.
2. Telegram client loads frontend assets over HTTPS.
3. Frontend initializes the Telegram Web Apps SDK.
4. Frontend sends Telegram `initData` to the backend.
5. Backend validates `initData`.
6. Backend returns authenticated user/session data.
7. Frontend renders application UI inside Telegram.

## 6. Security Baseline

The platform must:

- Use HTTPS in production
- Keep secrets outside git
- Validate Telegram webhook secret token in production
- Validate Mini App `initData` server-side
- Treat all user input as untrusted
- Use least-privilege database credentials
- Avoid logging secrets or raw authentication payloads
- Fail fast on invalid configuration

Detailed controls are defined in `SECURITY_REQUIREMENTS.md`.

## 7. Recommended Repository Structure

```text
repo/
  README.md

  docs/
    PROJECT_BRIEF.md
    PRD.md
    ARCHITECTURE.md
    RUNBOOK.md
    CODING_STANDARDS.md
    TESTING_REQUIREMENTS.md
    SECURITY_REQUIREMENTS.md

  backend/
    app/
      main.py
      config.py
      logging.py

      api/
      bot/
      db/
      models/
      repositories/
      services/
      storage/
      tests/

    alembic/
    pyproject.toml
    Dockerfile

  frontend/
    src/
    public/
    package.json
    tsconfig.json
    vite.config.ts

  deploy/
    apache/
    systemd/
    scripts/
    docker-compose.yml
    .env.example

  .github/
    workflows/

```

## 8. Development Priorities

1. Register bot through BotFather.
2. Create backend service skeleton.
3. Add health and readiness endpoints.
4. Implement Telegram webhook endpoint.
5. Implement `/start` and `/help`.
6. Add PostgreSQL persistence.
7. Add Mini App frontend shell.
8. Validate Mini App authentication.
9. Add structured logging.
10. Add file storage abstraction.
11. Add deployment assets.
12. Add CI and automated tests.

## 9. Non-Goals for Initial Version

Initial version does not include:

- MTProto client implementation
- User account automation
- Payment processing
- Multi-region deployment
- Full SaaS tenancy
- Advanced analytics
- Complex admin console

Admin functionality is optional and may be added later.

## 10. AI Agent Guidance

When generating code:

- Prefer small, explicit modules
- Keep Telegram-specific code isolated
- Keep business logic independent from HTTP/webhook transport
- Use typed schemas and models
- Include migrations for schema changes
- Include tests with feature work
- Do not hardcode credentials
- Do not use polling unless explicitly required
- Keep local development runnable with Docker Compose
