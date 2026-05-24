<!-- docs/RUNBOOK.md -->

# Operational Runbook

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

This runbook describes operational procedures for:

- Server setup
- Local development
- Environment configuration
- Database setup
- TLS configuration
- Telegram webhook registration
- Deployment
- Logging
- Monitoring
- Backup and recovery
- Troubleshooting

## 2. Infrastructure Assumptions

Preferred baseline:

| Component | Default |
|---|---|
| OS | Ubuntu 22.04 |
| Reverse proxy | Apache2 |
| Backend | Python FastAPI |
| Database | PostgreSQL |
| Frontend | TypeScript build |
| TLS | Let’s Encrypt |
| SCM | GitHub |
| Hosting | AWS-compatible Linux host |

## 3. Initial Server Preparation

### 3.1 Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 3.2 Install Base Packages

```bash
sudo apt install -y \
  git \
  curl \
  unzip \
  apache2 \
  certbot \
  python3-certbot-apache \
  postgresql \
  postgresql-contrib \
  python3 \
  python3-pip \
  python3-venv
```

### 3.3 Install Node.js LTS

Do not rely blindly on the default Ubuntu repository version.

Example using NodeSource:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

Verify:

```bash
node --version
npm --version
```

## 4. Application User

Create a non-root application user:

```bash
sudo useradd --system --create-home --shell /usr/sbin/nologin app
```

Create application directories:

```bash
sudo mkdir -p /opt/app
sudo chown app:app /opt/app
```

## 5. Repository Setup

Clone repository:

```bash
cd /opt/app
sudo -u app git clone <repo-url> source
cd /opt/app/source
```

## 6. Backend Environment

```bash
cd /opt/app/source/backend

python3 -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt
```

If the project uses `pyproject.toml`, use the project-specific install command documented in `README.md`.

## 7. Frontend Environment

```bash
cd /opt/app/source/frontend

npm install
npm run build
```

Build artifacts should be copied or deployed to the configured frontend web root.

Example:

```bash
sudo mkdir -p /var/www/frontend
sudo cp -r dist/* /var/www/frontend/
```

## 8. Environment Configuration

### 8.1 Create Environment File

```bash
cp .env.example .env
```

For production, keep the environment file readable only by the application user and administrators:

```bash
sudo chown app:app /opt/app/source/.env
sudo chmod 600 /opt/app/source/.env
```

### 8.2 Minimum Required Variables

```text
APP_ENV=production
APP_PUBLIC_BASE_URL=https://example.com

BOT_TOKEN=
BOT_WEBHOOK_SECRET=

DATABASE_URL=

FRONTEND_PUBLIC_URL=https://example.com

FILE_STORAGE_PROVIDER=local
LOCAL_FILE_STORAGE_PATH=/opt/app/storage

AWS_REGION=
S3_BUCKET=

LOG_LEVEL=INFO
```

## 9. PostgreSQL Setup

### 9.1 Create Database User and Database

```bash
sudo -u postgres createuser --pwprompt app_user
sudo -u postgres createdb --owner=app_user telegram_bot
```

### 9.2 Verify Access

Use a plain PostgreSQL URL for `psql`:

```bash
psql "postgresql://app_user:<password>@localhost:5432/telegram_bot"
```

### 9.3 Application Database URL

The backend may use a SQLAlchemy-compatible URL:

```text
postgresql+psycopg://app_user:<password>@localhost:5432/telegram_bot
```

## 10. Database Migrations

Run migrations:

```bash
cd /opt/app/source/backend
source .venv/bin/activate

alembic upgrade head
```

## 11. Backend Startup

### 11.1 Development Mode

```bash
uvicorn app.main:app --reload
```

### 11.2 Production Mode

```bash
gunicorn \
  -k uvicorn.workers.UvicornWorker \
  app.main:app \
  --bind 127.0.0.1:8000
```

## 12. Apache2 Configuration

### 12.1 Enable Required Modules

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod headers
```

### 12.2 Example VirtualHost

```apache
<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / https://example.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName example.com

    DocumentRoot /var/www/frontend

    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Proto "https"

    ProxyPass /api http://127.0.0.1:8000/api
    ProxyPassReverse /api http://127.0.0.1:8000/api

    ProxyPass /telegram/webhook http://127.0.0.1:8000/telegram/webhook
    ProxyPassReverse /telegram/webhook http://127.0.0.1:8000/telegram/webhook

    ProxyPass /health http://127.0.0.1:8000/health
    ProxyPassReverse /health http://127.0.0.1:8000/health

    ProxyPass /ready http://127.0.0.1:8000/ready
    ProxyPassReverse /ready http://127.0.0.1:8000/ready

    <Directory /var/www/frontend>
        Require all granted
        Options -Indexes
        AllowOverride None
    </Directory>
</VirtualHost>
```

Enable site and reload:

```bash
sudo a2ensite <site-config-name>
sudo apachectl configtest
sudo systemctl reload apache2
```

## 13. TLS Configuration

Obtain Let’s Encrypt certificate:

```bash
sudo certbot --apache
```

Verify renewal timer:

```bash
sudo systemctl status certbot.timer
```

Certbot can manage certificate directives automatically when using the Apache plugin.

## 14. systemd Service

Create service file:

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Example:

```ini
[Unit]
Description=Telegram Bot Backend
After=network.target postgresql.service

[Service]
User=app
Group=app
WorkingDirectory=/opt/app/source/backend
EnvironmentFile=/opt/app/source/.env
ExecStart=/opt/app/source/backend/.venv/bin/gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Reload and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service
sudo systemctl status telegram-bot.service
```

## 15. Telegram Bot Registration

Create bot through BotFather:

```text
/newbot
```

Store the generated bot token securely.

## 16. Telegram Webhook Setup

Register webhook:

```bash
curl -X POST \
  "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
  -d "url=https://example.com/telegram/webhook" \
  -d "secret_token=<WEBHOOK_SECRET>"
```

Verify webhook:

```bash
curl \
  "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"
```

## 17. Health Checks

Liveness:

```bash
curl https://example.com/health
```

Readiness:

```bash
curl https://example.com/ready
```

## 18. Standard Deployment Procedure

1. Pull latest changes.
2. Install/update backend dependencies.
3. Install/update frontend dependencies.
4. Run database migrations.
5. Build frontend.
6. Deploy frontend assets.
7. Restart backend service.
8. Reload Apache if configuration changed.
9. Check `/health`.
10. Check `/ready`.
11. Check Telegram webhook info.
12. Run smoke test through Telegram.

Example:

```bash
cd /opt/app/source
sudo -u app git pull

cd backend
sudo -u app .venv/bin/pip install -r requirements.txt
sudo -u app .venv/bin/alembic upgrade head

cd ../frontend
sudo -u app npm install
sudo -u app npm run build

sudo cp -r dist/* /var/www/frontend/

sudo systemctl restart telegram-bot.service
curl https://example.com/health
curl https://example.com/ready
```

## 19. Logs

### 19.1 Backend Logs

```bash
journalctl -u telegram-bot.service -f
```

### 19.2 Apache Logs

```bash
sudo tail -f /var/log/apache2/access.log
sudo tail -f /var/log/apache2/error.log
```

### 19.3 PostgreSQL Status

```bash
sudo systemctl status postgresql
```

## 20. Backups

### 20.1 PostgreSQL Backup

```bash
pg_dump "postgresql://app_user:<password>@localhost:5432/telegram_bot" > backup.sql
```

### 20.2 PostgreSQL Restore

```bash
psql "postgresql://app_user:<password>@localhost:5432/telegram_bot" < backup.sql
```

### 20.3 Local File Storage Backup

```bash
tar -czf storage-backup.tar.gz /opt/app/storage
```

### 20.4 S3 Storage Backup

Use bucket versioning, lifecycle policies, and replication where appropriate.

## 21. Troubleshooting

### 21.1 Telegram Webhook Not Receiving Updates

Possible causes:

- Invalid HTTPS certificate
- Wrong webhook URL
- Backend service down
- Apache proxy misconfiguration
- Invalid DNS
- Firewall blocking traffic

Diagnostics:

```bash
curl https://example.com/health
curl https://example.com/ready
curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"
sudo journalctl -u telegram-bot.service -n 100
sudo tail -n 100 /var/log/apache2/error.log
```

### 21.2 Mini App Authentication Fails

Possible causes:

- Invalid `initData` validation
- Wrong bot token
- Expired auth timestamp
- Frontend not sending expected data

Diagnostics:

- Check backend auth logs.
- Confirm frontend sends Telegram `initData`.
- Verify server clock is correct.
- Review HMAC validation implementation.

### 21.3 Database Connection Errors

Possible causes:

- PostgreSQL not running
- Invalid credentials
- Wrong database URL format
- Database unavailable

Diagnostics:

```bash
sudo systemctl status postgresql
psql "postgresql://app_user:<password>@localhost:5432/telegram_bot"
```

If the application uses:

```text
postgresql+psycopg://app_user:<password>@localhost:5432/telegram_bot
```

convert to the following for `psql`:

```text
postgresql://app_user:<password>@localhost:5432/telegram_bot
```

### 21.4 TLS Issues

Diagnostics:

```bash
sudo certbot certificates
openssl s_client -connect example.com:443
```

## 22. Security Checklist Before Production

- HTTPS enabled
- Debug mode disabled
- Secrets outside git
- Bot token stored securely
- Webhook secret configured
- Database password strong
- Firewall configured
- Application runs as non-root user
- Backups configured
- Logs reviewed for sensitive data
- `/health` and `/ready` available

## 23. Disaster Recovery Order

1. Restore infrastructure.
2. Restore PostgreSQL.
3. Restore file storage.
4. Restore environment configuration.
5. Start backend service.
6. Verify `/health`.
7. Verify `/ready`.
8. Verify Telegram webhook.
9. Verify Mini App behavior.

## 24. AI Agent Operational Guidance

When generating operational assets:

- Prefer explicit commands.
- Avoid hidden assumptions.
- Use environment variables.
- Do not hardcode secrets.
- Keep startup deterministic.
- Keep deployment reproducible.
