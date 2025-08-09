# ZerologsVPN Subscription Server

Production-ready **FastAPI** service that issues VPN subscription configs (VLESS/REALITY) for v2rayN/v2rayNG, Clash, and sing-box.
- **PostgreSQL** as the source of truth for UID pool.
- **Redis** for future sidecar events (publish `uid.assign` / `uid.revoke`). Sidecar is out-of-repo.
- **Alembic** migrations.
- **Dockerized**. `docker-compose.yml` for quick deploy.

## Quick Start (Docker)
```bash
git clone <your-repo-url> subscription-server
cd subscription-server
cp .env.production.example .env
# IMPORTANT: change passwords/secrets in .env
docker compose up -d --build
# auto-migrates DB, then starts API on :8080
```

### Seed UUIDs
```bash
docker compose exec api python -m subscription_server.app.seed_uuids --count 500
```

### API Docs
- http://localhost:8080/docs

## Environment
Copy `.env.production.example` to `.env` and edit:
- `POSTGRES_*` for database
- `DB_DSN` (overrides POSTGRES_* if set)
- `REDIS_URL` for Redis
- `HMAC_SECRET` for link signatures
- `HOSTNAME`, `XRAY_PORT`, and REALITY params for output config

## Admin Flow
1) **Assign a UID**:
```bash
curl -sX POST http://localhost:8080/api/admin/assign -H 'Content-Type: application/json' -d '{"user_id":12345,"plan_id":1}'
```
2) **Generate a link**:
```bash
curl -sX POST http://localhost:8080/api/admin/link -H 'Content-Type: application/json' -d '{"uid":"<UUID>","fmt":"txt"}'
```
3) Open returned `/sub/<uid>[.yaml|.json]`.

## Route Examples

- **Health check**
  ```bash
  curl http://localhost:8080/health
  ```
- **Revoke a UID**
  ```bash
  curl -sX POST http://localhost:8080/api/admin/revoke \
       -H 'Content-Type: application/json' \
       -d '{"uid":"<UUID>"}'
  ```
- **Retrieve subscription config**
  ```bash
  curl "http://localhost:8080/sub/<UID>?sig=<SIG>&exp=<EXP>"
  curl "http://localhost:8080/sub/<UID>.yaml?sig=<SIG>&exp=<EXP>"
  curl "http://localhost:8080/sub/<UID>.json?sig=<SIG>&exp=<EXP>"
  ```

## Tests
```bash
pip install -r requirements.txt
pytest -q
```
