<!-- docs/TESTING_REQUIREMENTS.md -->

# Testing Requirements

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

This document defines testing requirements for the Telegram Bot Platform.

Goals:

- Ensure functional correctness
- Prevent regressions
- Validate security-sensitive behavior
- Improve deployment confidence
- Support AI-assisted development
- Keep critical behavior reproducible

## 2. Testing Principles

- Prefer automated tests over manual validation.
- Tests must be deterministic.
- Tests must be isolated.
- Tests must be reproducible.
- Tests must validate behavior, not implementation details.
- Security-sensitive flows require positive and negative tests.
- Production credentials must never be used in tests.

## 3. Required Test Categories

| Category | Required | Purpose |
|---|---|---|
| Unit tests | Yes | Validate isolated logic |
| Integration tests | Yes | Validate component interactions |
| API tests | Yes | Validate HTTP interfaces |
| Database tests | Yes | Validate persistence behavior |
| Security tests | Yes | Validate authentication and authorization |
| End-to-end tests | Preferred | Validate complete workflows |
| Load tests | Optional initially | Validate scalability assumptions |

## 4. Backend Unit Tests

### 4.1 Scope

Unit tests must validate:

- Business logic
- Command handlers
- Dispatcher behavior
- Services
- Validation logic
- Configuration parsing
- Authentication logic
- Utility functions

### 4.2 Required Unit Tests

| Component | Required |
|---|---|
| Command dispatcher | Yes |
| `/start` handler | Yes |
| `/help` handler | Yes |
| `/status` handler | Yes |
| Unknown command handler | Yes |
| Mini App auth validation | Yes |
| Storage abstraction | Yes |
| Configuration parsing | Yes |
| User service | Yes |

### 4.3 Requirements

Unit tests must:

- Avoid real network calls.
- Avoid production services.
- Avoid shared mutable state.
- Execute quickly.
- Be deterministic.

Suggested location:

```text
backend/app/tests/unit/
```

## 5. Backend Integration Tests

### 5.1 Scope

Integration tests validate interactions between:

- API and database
- Service and repository
- Webhook and dispatcher
- Storage and metadata persistence
- Migration and schema state

### 5.2 Required Integration Tests

| Flow | Required |
|---|---|
| Telegram webhook processing | Yes |
| User persistence | Yes |
| Mini App authentication | Yes |
| File metadata persistence | Yes |
| Database migrations | Yes |

### 5.3 Requirements

Integration tests should:

- Use isolated databases.
- Use test-specific configuration.
- Avoid production services.
- Clean up state after execution.

Suggested location:

```text
backend/app/tests/integration/
```

## 6. API Testing

### 6.1 Required Endpoints

| Endpoint | Required |
|---|---|
| `/health` | Yes |
| `/ready` | Yes |
| `/telegram/webhook` | Yes |
| `/api/me` | Yes |
| `/api/example-action` | Yes |

### 6.2 Required Coverage

API tests must validate:

- Status codes
- Request validation
- Response schemas
- Authentication
- Authorization where applicable
- Error responses
- Invalid JSON
- Missing authentication
- Malformed inputs

## 7. Database Testing

### 7.1 Required Validation

Database tests must validate:

- Schema creation
- Migration application
- Constraints
- Relationships
- Repository behavior
- UTC timestamp handling

### 7.2 Migration Testing

Every migration must:

- Apply cleanly to an empty database.
- Apply cleanly to the current schema.
- Preserve existing data correctly where applicable.
- Be reviewed for destructive changes.

Downgrade testing is required only if the project supports downgrade migrations.

If downgrade migrations are not supported, this must be documented.

### 7.3 Isolation

Tests must use:

- Dedicated test database, or
- Temporary schemas, or
- Transaction rollback strategy

Production databases must never be used for tests.

## 8. Telegram Bot Testing

### 8.1 Webhook Scenarios

| Scenario | Required |
|---|---|
| Valid update | Yes |
| Invalid payload | Yes |
| Invalid secret token | Yes |
| Missing secret token in production | Yes |
| Unsupported update type | Yes |
| Unknown command | Yes |

### 8.2 Command Scenarios

| Command | Required |
|---|---|
| `/start` | Yes |
| `/help` | Yes |
| `/status` | Yes |
| Unknown command | Yes |

Command tests must validate:

- Response generation
- User persistence behavior
- Permission handling where applicable
- Error behavior

## 9. Mini App Testing

### 9.1 Frontend Testing

Required frontend coverage:

| Area | Required |
|---|---|
| Application bootstrap | Yes |
| Telegram SDK integration | Yes |
| API client | Yes |
| Authentication handling | Yes |
| Error handling | Yes |

Suggested location:

```text
frontend/src/tests/
```

### 9.2 Mini App Authentication Testing

Backend tests must validate:

- Valid Telegram `initData`
- Invalid signature
- Expired timestamp
- Missing user payload
- Modified payload
- Missing authentication header or payload

This is security-critical.

## 10. File Storage Testing

Required tests:

| Feature | Required |
|---|---|
| File save | Yes |
| File retrieval | Yes |
| File deletion | Yes |
| Metadata persistence | Yes |
| Invalid file handling | Yes |
| Path traversal prevention | Yes |
| Filename sanitization | Yes |

## 11. Security Testing

Security requirements are defined in `SECURITY_REQUIREMENTS.md`.

Mandatory security tests:

| Area | Required |
|---|---|
| Webhook secret validation | Yes |
| Mini App auth validation | Yes |
| Unauthorized API access | Yes |
| Invalid payload handling | Yes |
| File validation | Yes |

Tests must ensure:

- Invalid auth is rejected.
- Unsafe file paths are rejected.
- Secrets are not exposed in responses.
- Sensitive values are not logged where practical to test.

## 12. Frontend Test Standards

Preferred tooling:

- vitest
- testing-library
- eslint
- prettier

Avoid fragile pixel-perfect testing initially.

Focus on:

- Rendering
- API integration
- State transitions
- Error states
- Telegram SDK integration

## 13. CI/CD Testing Requirements

CI must include:

| Step | Required |
|---|---|
| Formatting check | Yes |
| Linting | Yes |
| Type checking | Yes |
| Unit tests | Yes |
| Integration tests | Yes |
| Migration validation | Yes |
| Frontend build validation | Yes |

CI must fail if:

- Tests fail.
- Linting fails.
- Type checking fails.
- Migration validation fails.
- Build validation fails.

## 14. Code Coverage Expectations

Initial targets:

| Area | Minimum |
|---|---|
| Core services | 80% |
| Security-sensitive code | 90% |
| Utility modules | 70% |
| Frontend critical flows | 70% |

Coverage targets are guidelines. Meaningful tests matter more than raw percentage.

## 15. Mocking Standards

Allowed mocking:

- Telegram Bot API
- S3 APIs
- External HTTP APIs
- Time providers
- Random/UUID providers where determinism is needed

Avoid excessive mocking of:

- Core business logic
- Repository behavior in integration tests
- Authentication algorithms

## 16. Test Data Standards

Test data must:

- Be synthetic.
- Be deterministic.
- Use fake Telegram IDs.
- Avoid real bot tokens.
- Avoid production database dumps.
- Avoid personal user data.

## 17. Recommended Backend Tooling

| Tool | Purpose |
|---|---|
| pytest | Test runner |
| pytest-asyncio | Async testing |
| pytest-cov | Coverage |
| httpx | API testing |
| factory_boy | Test fixtures |
| faker | Synthetic data |

## 18. Recommended Frontend Tooling

| Tool | Purpose |
|---|---|
| vitest | Frontend tests |
| testing-library | UI testing |
| eslint | Linting |
| prettier | Formatting |

## 19. Recommended Commands

Backend tests:

```bash
pytest
```

Backend coverage:

```bash
pytest --cov=app
```

Backend linting:

```bash
ruff check .
mypy .
```

Frontend tests:

```bash
npm run test
```

Frontend linting:

```bash
npm run lint
```

## 20. Definition of Testing Completion

A feature is sufficiently tested when:

- Happy path is validated.
- Negative paths are validated.
- Security-sensitive behavior is validated.
- Relevant automated tests are added.
- CI passes.
- No flaky tests are introduced.
- No production services are required for test execution.

## 21. AI Agent Testing Rules

AI-generated features must include:

- Unit tests.
- Integration tests where applicable.
- Edge-case validation.
- Negative-path validation.
- Security tests for auth or input handling changes.

AI agents must not:

- Disable failing tests.
- Remove tests to satisfy CI.
- Generate tests that depend on production services.
- Use real credentials.
- Skip security-sensitive test cases.
