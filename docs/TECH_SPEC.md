# TECH_SPEC.md – auth‑licence

---

## 1. Overview

`auth‑licence` is a lightweight, self‑contained service that supplies:

| Feature | Description |
|---------|-------------|
| **User Authentication** | JWT‑based login with optional OAuth2 providers (Google, GitHub). |
| **License Management** | Per‑user or per‑app license keys, with activation limits, expiry, and usage quotas. |
| **API Gateway** | Exposes a REST/GraphQL endpoint for client apps to validate tokens and license status. |
| **Admin Console** | Web UI for managing users, licenses, and viewing usage analytics. |

Target audience: solo founders and small SaaS teams who need a plug‑and‑play solution without maintaining a full‑blown auth stack.

---

## 2. Architecture

```
┌───────────────────────┐
│  Client App (Web/CLI) │
└─────────────┬─────────┘
              │
              ▼
┌───────────────────────┐
│  auth‑licence API      │
│  (FastAPI + GraphQL)   │
└───────┬───────┬───────┘
        │       │
        ▼       ▼
┌───────────────┐ ┌───────────────────────┐
│ Auth Service  │ │ License Service        │
│ (JWT/OAuth2)  │ │ (Key generation,      │
│               │ │ quota enforcement)    │
└───────┬───────┘ └───────┬─────────────────┘
        │               │
        ▼               ▼
┌───────────────────────┐
│  PostgreSQL 12        │
│  (schema: users,      │
│   licenses, usage)    │
└───────┬───────┬───────┘
        │       │
        ▼       ▼
┌───────────────────────┐
│ Redis 7 (cache)       │
└───────────────────────┘
```

* **FastAPI** – high‑performance async framework, auto‑generates OpenAPI docs.  
* **GraphQL** – optional, for clients that prefer flexible queries.  
* **JWT** – stateless authentication; signed with RSA‑2048.  
* **OAuth2** – optional social login via `Authlib`.  
* **PostgreSQL** – durable storage; ACID guarantees for license state.  
* **Redis** – short‑lived cache for token introspection and rate‑limiting.  
* **Docker Compose** – local dev stack.  
* **Kubernetes** – production deployment (Helm chart).  

---

## 3. Data Model

| Table | Columns | Notes |
|-------|---------|-------|
| **users** | `id (UUID PK)`, `email (unique)`, `hashed_password`, `created_at`, `updated_at` | Passwords stored with Argon2id. |
| **oauth_providers** | `id`, `user_id FK`, `provider`, `provider_user_id`, `access_token`, `refresh_token` | Optional. |
| **licenses** | `id (UUID PK)`, `user_id FK`, `app_name`, `key (unique)`, `issued_at`, `expires_at`, `max_activations`, `activations`, `quota_mb`, `quota_used_mb` | `key` is a base32 string. |
| **activations** | `id`, `license_id FK`, `device_id`, `activated_at`, `last_seen_at` | Tracks each device. |
| **usage** | `id`, `license_id FK`, `timestamp`, `bytes_used` | For quota enforcement. |

Indexes on `email`, `key`, `user_id` for fast lookups.

---

## 4. Key APIs / Interfaces

### 4.1 REST Endpoints (OpenAPI)

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| POST | `/auth/register` | Create user | None |
| POST | `/auth/login` | Issue JWT | None |
| POST | `/auth/oauth/callback` | OAuth2 callback | None |
| GET | `/auth/me` | Current user profile | Bearer |
| POST | `/licenses` | Create license | Bearer |
| GET | `/licenses/{id}` | Get license details | Bearer |
| POST | `/licenses/{id}/activate` | Activate license on device | Bearer |
| POST | `/licenses/{id}/deactivate` | Deactivate device | Bearer |
| GET | `/usage` | Current usage stats | Bearer |

### 4.2 GraphQL Schema (optional)

```
type User { id: ID!, email: String! }
type License { id: ID!, key: String!, appName: String!, expiresAt: DateTime! }
type Query { me: User, license(id: ID!): License }
type Mutation {
  register(email: String!, password: String!): AuthPayload
  login(email: String!, password: String!): AuthPayload
  createLicense(appName: String!, maxActivations: Int, quotaMb: Int): License
  activateLicense(id: ID!, deviceId: String!): Activation
}
```

### 4.3 Admin Console

* Built with **React** + **Material‑UI**.  
* Exposes same REST endpoints under `/admin`.  
* Authenticated via JWT with `admin` role flag.

---

## 5. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **API** | FastAPI (Python 3.11) | Async, type‑safe, auto‑docs |
| **Auth** | PyJWT, Authlib | Standard JWT/OAuth2 libraries |
| **DB** | PostgreSQL 12 | Mature, ACID, supports JSONB |
| **Cache** | Redis 7 | Fast token introspection |
| **Container** | Docker, Docker‑Compose | Reproducible dev environment |
| **Orchestration** | Kubernetes + Helm | Scalable, self‑healing |
| **CI/CD** | GitHub Actions | Lint, test, build, push |
| **Monitoring** | Prometheus + Grafana | Metrics, alerts |
| **Logging** | Loguru + Loki | Structured logs |

---

## 6. Dependencies

| Category | Package | Version |
|----------|---------|---------|
| FastAPI | `fastapi` | ^0.110.0 |
| Auth | `pyjwt` | ^2.8.0 |
| Auth | `authlib` | ^1.2.0 |
| DB | `asyncpg` | ^0.29.0 |
| ORM | `SQLAlchemy` | ^2.0.30 |
| Migrations | `alembic` | ^1.13.0 |
| Cache | `aioredis` | ^2.0.1 |
| Testing | `pytest` | ^8.2.0 |
| Lint | `ruff` | ^0.4.0 |
| Docker | `docker` | - |
| Kubernetes | `helm` | ^3.15.0 |

All dependencies are pinned in `pyproject.toml` and `requirements.txt`.

---

## 7. Deployment

### 7.1 Local Development

```bash
docker compose up --build
```

* API available at `http://localhost:8000`.
* Admin UI at `http://localhost:3000`.

### 7.2 Production

1. **Helm Chart** – `charts/auth-licence/`
2. **Secrets** – Store DB credentials, JWT keys, OAuth secrets in Kubernetes Secrets.
3. **Ingress** – TLS termination via cert‑manager.
4. **Horizontal Pod Autoscaler** – Scale API pods based on CPU/memory.
5. **Database** – Managed PostgreSQL (e.g., RDS) with automated backups.
6. **Cache** – Managed Redis (e.g., Elasticache) with persistence.
7. **Observability** – Prometheus scrape, Loki for logs, Grafana dashboards.

---

## 8. Security Considerations

| Area | Mitigation |
|------|------------|
| JWT Secret | RSA‑2048 key pair, stored in KMS. |
| Password Storage | Argon2id with per‑user salt. |
| Rate Limiting | Redis‑based token bucket per IP. |
| Input Validation | Pydantic models, OpenAPI schema. |
| CORS | Strict policy, allow only whitelisted origins. |
| Secrets | Never commit; use GitHub Secrets / KMS. |

---

## 9. Testing Strategy

| Type | Tool | Coverage |
|------|------|----------|
| Unit | `pytest` + `pytest-asyncio` | 90% |
| Integration | `httpx` test client | 80% |
| End‑to‑End | Cypress (Admin UI) | 70% |
| Security | `bandit`, `safety` | Continuous |

Test data is seeded via Alembic migration scripts.

---

## 10. Roadmap (next 6 months)

1. **OAuth2 Provider Support** – Google & GitHub.  
2. **Webhooks** – Notify clients on license expiry.  
3. **Multi‑tenant DB** – Separate schemas per customer.  
4. **Analytics API** – Usage dashboards.  
5. **CLI Tool** – For developers to manage licenses locally.  

---

## 11. Contact & Maintenance

* **Repository**: `arkashira/auth-licence`  
* **Issue Tracker**: GitHub Issues  
* **Slack Channel**: `#auth-licence`  
* **Maintainer**: Senior Product Engineer – `alice@axentx.com`

---
