<!-- docs/CODING_STANDARDS.md -->

# Coding Standards

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

This document defines coding standards for the Telegram Bot Platform.

The standards apply to:

- Backend code
- Frontend code
- Infrastructure code
- Database migrations
- Tests
- Documentation

## 2. General Principles

- Prefer explicitness over magic.
- Prefer readability over cleverness.
- Keep modules small.
- Keep responsibilities narrow.
- Avoid premature abstraction.
- Keep dependencies minimal.
- Separate transport logic from business logic.
- Fail fast on invalid configuration.
- Write deterministic code where practical.

## 3. Repository Standards

### 3.1 Repository Structure

Use the approved layout:

```text
repo/
  backend/
  frontend/
  deploy/
  docs/
  .github/
```

Avoid unrelated top-level directories.

### 3.2 Documentation Naming

Documentation files use uppercase names with underscores:

```text
PROJECT_BRIEF.md
PRD.md
ARCHITECTURE.md
RUNBOOK.md
CODING_STANDARDS.md
TESTING_REQUIREMENTS.md
SECURITY_REQUIREMENTS.md
```

## 4. Backend Standards

### 4.1 Python Version

Use:

```text
Python 3.11+
```

### 4.2 Preferred Backend Stack

- FastAPI
- SQLAlchemy 2.x or SQLModel
- Alembic
- pytest
- ruff
- mypy
- black
- isort

### 4.3 Formatting

Use:

- black
- isort
- ruff

Line length:

```text
88
```

### 4.4 Type Checking

Use:

- mypy

Type hints are required for:

- Public functions
- API handlers
- Service methods
- Repository methods
- Security-sensitive functions

Example:

```python
def create_user(
    telegram_user_id: int,
    username: str | None,
) -> User:
    ...
```

### 4.5 Imports

Preferred:

```python
from app.services.user_service import UserService
```

Forbidden:

```python
from app.services import *
```

Wildcard imports are not allowed.

### 4.6 Function Design

Functions should:

- Have one responsibility.
- Be short and readable.
- Avoid hidden side effects.
- Return predictable outputs.
- Use explicit parameters.

Avoid functions that:

- Mix IO and business logic.
- Mutate unrelated state.
- Catch broad exceptions unnecessarily.

### 4.7 Exception Handling

Allowed:

```python
try:
    ...
except ExpectedError as exc:
    logger.warning("Expected operation failed", exc_info=exc)
```

Forbidden:

```python
try:
    ...
except Exception:
    pass
```

Do not silently suppress errors.

### 4.8 Configuration Access

Preferred:

```python
settings.database_url
```

Avoid direct environment access outside configuration modules:

```python
os.getenv("DATABASE_URL")
```

### 4.9 Logging

Logs must not contain:

- Bot tokens
- Passwords
- API secrets
- Session secrets
- Raw authentication payloads

Use structured logging where practical.

## 5. API Standards

### 5.1 Endpoint Naming

Preferred:

```text
/api/me
/api/users
/api/files
```

Avoid:

```text
/api/getUserData
```

### 5.2 Response Shape

Success:

```json
{
  "status": "success",
  "data": {}
}
```

Error:

```json
{
  "status": "error",
  "error": {
    "code": "invalid_request",
    "message": "Invalid request"
  }
}
```

### 5.3 HTTP Status Codes

| Status | Usage |
|---|---|
| 200 | Success |
| 201 | Created |
| 400 | Invalid request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 409 | Conflict |
| 500 | Internal server error |

## 6. Telegram Bot Standards

### 6.1 Command Handling

Each command should:

- Have isolated handler logic.
- Be independently testable.
- Avoid direct database access from the transport layer.
- Return predictable response objects.

### 6.2 Telegram-Specific Logic

Keep Telegram integration code under:

```text
backend/app/bot/
```

Do not spread Telegram-specific parsing or Bot API calls across unrelated modules.

### 6.3 Webhook Handling

Webhook handlers should:

- Validate payloads.
- Validate secret token in production.
- Return quickly.
- Avoid long blocking tasks.

## 7. Mini App Standards

### 7.1 Frontend Stack

Preferred:

- TypeScript
- Vite
- Telegram Web Apps SDK

### 7.2 Frontend Rules

- Keep components small.
- Avoid deeply nested state.
- Avoid global mutable state where practical.
- Keep API calls in a dedicated client module.
- Handle loading and error states.

### 7.3 Authentication Rules

Never trust frontend user identity directly.

Backend must validate Telegram `initData`.

## 8. Database Standards

### 8.1 Engine

Use:

```text
PostgreSQL
```

### 8.2 Migrations

All schema changes must use migrations.

Do not manually change production schema outside migration process.

### 8.3 Naming

Tables:

```text
snake_case_plural
```

Examples:

```text
users
chat_sessions
audit_logs
```

Columns:

```text
snake_case
```

### 8.4 Timestamps

Persistent entities should include:

```text
created_at
updated_at
```

Use UTC timestamps.

## 9. File Storage Standards

Application logic must not directly depend on:

- Local filesystem implementation details
- S3 SDK implementation details

Use:

```text
backend/app/storage/
```

Generated file identifiers should use:

- UUIDs
- Sanitized names
- Controlled storage keys

Never trust raw user-provided filenames.

## 10. Testing Standards

Detailed testing requirements are defined in `TESTING_REQUIREMENTS.md`.

Basic rule:

- New features require tests.
- Security-sensitive logic requires negative-path tests.
- Do not remove tests to satisfy CI.

## 11. Security Standards

Detailed security requirements are defined in `SECURITY_REQUIREMENTS.md`.

Minimum rules:

- Do not commit secrets.
- Do not log secrets.
- Validate external input.
- Use parameterized queries.
- Validate Telegram auth.
- Keep admin routes protected when implemented.

## 12. Git Standards

### 12.1 Branch Naming

Preferred:

```text
feature/<name>
bugfix/<name>
hotfix/<name>
```

### 12.2 Commit Messages

Preferred:

```text
Add webhook secret validation
Fix Mini App auth parsing
Refactor user repository
```

Avoid:

```text
fix stuff
changes
update
```

### 12.3 Pull Requests

Each PR should include:

- Summary
- Scope
- Testing notes
- Migration notes, if applicable
- Security notes, if applicable

## 13. CI/CD Standards

CI should include:

- Formatting check
- Linting
- Type checking
- Unit tests
- Integration tests
- Frontend build validation
- Backend import/startup validation

CI must fail on:

- Test failure
- Lint failure
- Type-check failure
- Migration validation failure

## 14. Infrastructure Standards

Preferred future infrastructure tooling:

- Docker Compose
- Terraform
- Ansible

Environment separation:

```text
development
staging
production
```

Production secrets must not be shared with development or staging.

## 15. Performance Standards

### 15.1 API

- Avoid unnecessary database queries.
- Use pagination for collections.
- Avoid synchronous blocking operations where practical.
- Keep webhook responses fast.

### 15.2 Database

- Avoid N+1 queries.
- Use indexes intentionally.
- Keep transactions short.
- Avoid large unbounded queries.

## 16. AI Agent Development Rules

AI-generated code must:

- Follow repository structure.
- Include typing.
- Include tests.
- Avoid dead code.
- Avoid speculative abstractions.
- Avoid placeholder security logic.
- Avoid hidden global state.
- Update documentation when behavior changes.

AI-generated code must not:

- Hardcode credentials.
- Disable TLS validation.
- Suppress exceptions silently.
- Mix business logic with transport logic.
- Introduce unnecessary frameworks.
