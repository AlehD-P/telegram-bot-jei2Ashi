<!-- docs/ARCHITECTURE.md -->

# Architecture Document

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

## 1. Overview

This document describes the technical architecture of the Telegram Bot Platform.

The platform provides:

- Telegram Bot API webhook processing
- Telegram Mini App frontend
- Python backend APIs
- PostgreSQL persistence
- File storage abstraction
- Secure runtime configuration
- Linux deployment model

The architecture is optimized for:

- AI-assisted development
- Clear separation of concerns
- Incremental delivery
- Production readiness without unnecessary complexity

## 2. High-Level Architecture

```text
+------------------------------------------------------+
|                    Telegram Cloud                    |
|                                                      |
|  +------------------+    +------------------------+  |
|  | Telegram Users   |    | Telegram Bot API       |  |
|  +------------------+    +------------------------+  |
+------------------------------|-----------------------+
                               |
                               | HTTPS Webhook
                               |
+------------------------------v-----------------------+
|                  Public Linux Server                 |
|                                                      |
|  +------------------------------------------------+  |
|  | Apache2 Reverse Proxy                          |  |
|  |------------------------------------------------|  |
|  | TLS termination                                |  |
|  | Static frontend hosting                        |  |
|  | Reverse proxy to backend API                   |  |
|  +----------------------|-------------------------+  |
|                         |                            |
|                         v                            |
|  +------------------------------------------------+  |
|  | Python Backend / FastAPI                       |  |
|  |------------------------------------------------|  |
|  | Telegram webhook processing                    |  |
|  | Command dispatcher                             |  |
|  | Mini App API                                   |  |
|  | Authentication validation                      |  |
|  | Business logic                                 |  |
|  +----------------|-------------------------------+  |
|                   |                                  |
|        +----------+----------+                       |
|        |                     |                       |
|        v                     v                       |
|  +-----------+       +------------------+            |
|  | PostgreSQL|       | File Storage     |            |
|  | Database  |       | Local or S3      |            |
|  +-----------+       +------------------+            |
+------------------------------------------------------+
```

## 3. Architectural Principles

- Keep modules small and explicit.
- Separate transport logic from business logic.
- Keep Telegram-specific logic isolated.
- Keep persistence behind repositories.
- Keep storage behind an abstraction.
- Validate all external input.
- Keep runtime configuration centralized.
- Prefer simple deployment before complex orchestration.

## 4. Component Responsibilities

### 4.1 Telegram Layer

Responsibilities:

- Bot commands
- Messages
- Buttons
- Deep links
- Mini App launch

Integration method:

- Telegram Bot API
- HTTPS webhooks
- Telegram Web Apps SDK

Polling is not the default mode.

### 4.2 Apache2 Reverse Proxy

Responsibilities:

- TLS termination
- Static frontend hosting
- Reverse proxy to backend
- Security headers
- HTTP-to-HTTPS redirect

Example routing:

| Path | Destination |
|---|---|
| `/` | Frontend static assets |
| `/api/*` | Backend API |
| `/telegram/webhook` | Telegram webhook |
| `/health` | Backend liveness |
| `/ready` | Backend readiness |

### 4.3 Backend Service

Technology:

- Python 3.11+
- FastAPI
- Uvicorn or Gunicorn

Responsibilities:

- Telegram webhook handling
- Command dispatch
- Mini App APIs
- Telegram auth validation
- Business workflows
- Database access through repositories
- File access through storage abstraction

### 4.4 PostgreSQL

Responsibilities:

- Persist users
- Persist chats
- Persist sessions
- Persist update metadata
- Persist file metadata
- Persist audit events

### 4.5 File Storage

Responsibilities:

- Store uploaded files
- Store generated files
- Return controlled references to files
- Avoid exposing internal paths

Supported providers:

- Local filesystem
- S3-compatible object storage

## 5. Backend Internal Architecture

### 5.1 Layered Structure

```text
API Layer
    |
    v
Service Layer
    |
    v
Repository / Storage Layer
    |
    v
Database / File Storage
```

### 5.2 API Layer

Responsibilities:

- HTTP request parsing
- Authentication checks
- Request validation
- Response serialization
- Error mapping

Suggested modules:

```text
api/
  routes_health.py
  routes_telegram.py
  routes_miniapp.py
```

### 5.3 Bot Layer

Responsibilities:

- Telegram update parsing
- Command routing
- Telegram Bot API calls
- Bot response creation

Suggested modules:

```text
bot/
  dispatcher.py
  commands.py
  telegram_client.py
  schemas.py
```

### 5.4 Service Layer

Responsibilities:

- Business workflows
- User registration
- Session handling
- Mini App auth validation
- File orchestration

Suggested modules:

```text
services/
  user_service.py
  bot_service.py
  miniapp_auth_service.py
  file_service.py
```

### 5.5 Repository Layer

Responsibilities:

- Database queries
- Persistence operations
- Query encapsulation
- Transaction-friendly data access

Suggested modules:

```text
repositories/
  users.py
  chats.py
  sessions.py
  update_logs.py
  files.py
```

### 5.6 Storage Layer

Responsibilities:

- Abstract file operations
- Provide local and S3-compatible implementations
- Prevent unsafe file paths

Suggested modules:

```text
storage/
  base.py
  local.py
  s3.py
```

## 6. Telegram Webhook Flow

```text
Telegram Bot API
  |
  v
Apache2
  |
  v
FastAPI webhook endpoint
  |
  v
Webhook secret validation
  |
  v
Payload validation
  |
  v
Dispatcher
  |
  v
Command or event handler
  |
  +--> Services
  +--> Repositories
  +--> Storage
  |
  v
Telegram API response
```

Webhook handlers should be fast. Heavy work should be deferred to background processing in later versions.

## 7. Mini App Architecture

```text
Telegram Client
  |
  v
Mini App Frontend
  |
  v
Telegram Web Apps SDK
  |
  v
Backend API
  |
  v
Mini App initData validation
  |
  v
User/session services
```

### 7.1 Mini App Authentication

Frontend receives Telegram `initData`.

Backend validates:

- Signature
- Payload integrity
- Timestamp freshness
- User payload

Backend must not trust frontend-provided user IDs without validation.

## 8. Database Architecture

### 8.1 Initial Entities

| Entity | Purpose |
|---|---|
| User | Telegram user identity |
| Chat | Telegram chat metadata |
| Session | Runtime session state |
| UpdateLog | Incoming update metadata |
| FileObject | File metadata |
| AuditLog | Security/admin events |

### 8.2 Database Principles

- Use migrations for all schema changes.
- Store UTC timestamps.
- Use indexed foreign keys.
- Avoid unnecessary PII.
- Store raw updates only when explicitly configured.
- Keep database users least-privileged.

## 9. Configuration Architecture

### 9.1 Configuration Source Priority

```text
Explicit Environment Variables
    |
    v
Injected Secrets / Secret Store Values
    |
    v
Safe Application Defaults
```

### 9.2 Rules

- Application code must read configuration through a centralized settings module.
- Business logic must not call environment APIs directly.
- Secrets must not be logged.
- Startup must fail on missing critical configuration.

### 9.3 Required Configuration Categories

| Category | Examples |
|---|---|
| App | Environment, public URLs |
| Telegram | Bot token, webhook secret |
| Database | Connection string |
| Storage | Local path, S3 bucket |
| Logging | Log level |
| AWS | Region, credentials |

## 10. Logging and Monitoring Architecture

### 10.1 Logging Goals

- Operational visibility
- Debuggability
- Security auditability
- Consistent error reporting

### 10.2 Health Endpoints

| Endpoint | Purpose |
|---|---|
| `/health` | Process liveness |
| `/ready` | Dependency readiness |

### 10.3 Future Monitoring Options

Potential future integrations:

- Prometheus
- Grafana
- Loki
- CloudWatch
- Sentry

## 11. Security Architecture

Security controls are defined in detail in `SECURITY_REQUIREMENTS.md`.

Architecture-level controls:

- HTTPS in production
- Webhook secret validation
- Mini App `initData` validation
- Secrets outside source control
- Input validation
- Least-privilege database access
- Sanitized logging

## 12. Deployment Architecture

### 12.1 Initial Deployment

```text
Ubuntu 22.04
    |
    +--> Apache2
    +--> Python Backend
    +--> PostgreSQL
    +--> systemd services
```

### 12.2 Future Deployment Options

Possible future options:

- Docker Compose
- ECS/Fargate
- Kubernetes
- CDN-backed frontend hosting
- Managed PostgreSQL
- Managed object storage

## 13. CI/CD Architecture

Recommended pipeline:

```text
GitHub Push / Pull Request
    |
    v
Formatting
    |
    v
Linting
    |
    v
Type Checking
    |
    v
Tests
    |
    v
Build Validation
    |
    v
Deployment
```

## 14. Failure Handling

Principles:

- Fail fast on invalid configuration.
- Log unexpected exceptions.
- Return safe user-facing errors.
- Avoid leaking internal details.
- Keep webhook handlers idempotent where practical.

## 15. Scalability Notes

Initial architecture prioritizes simplicity.

Future scaling options:

- Horizontal backend replicas
- Background workers
- Queue-based processing
- Redis caching
- CDN for frontend
- Managed PostgreSQL
- S3-compatible object storage

## 16. AI Agent Guidance

When generating architecture-related code:

- Keep interfaces typed.
- Avoid unnecessary abstractions.
- Keep Telegram code isolated.
- Keep services testable.
- Keep deployment configurable.
- Update architecture docs when design changes.
