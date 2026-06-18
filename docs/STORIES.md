# STORIES.md

## Product: **auth‑licence**

A lightweight, plug‑and‑play authentication & licensing framework for solo founders and small SaaS developers.  
The goal is to protect web applications from piracy while keeping integration friction to a minimum.

---

## Epics & Story Backlog

| Epic | Story | Acceptance Criteria |
|------|-------|---------------------|
| **Core Authentication** | **E1‑S1** As a developer, I want to register a new user via a REST endpoint, so that I can create accounts for my SaaS. | • POST `/api/auth/register` accepts `email`, `password`, `name`. <br>• Returns 201 with JWT and user ID. <br>• Passwords are hashed with Argon2. <br>• Duplicate emails are rejected with 409. |
| | **E1‑S2** As a developer, I want to log in with email/password, so that users can access the app. | • POST `/api/auth/login` returns JWT, refresh token. <br>• 401 on wrong credentials. <br>• Rate‑limit to 5 attempts/min per IP. |
| | **E1‑S3** As a developer, I want to refresh a JWT, so that users stay logged in without re‑authenticating. | • POST `/api/auth/refresh` with refresh token returns new JWT. <br>• Refresh token expires after 30 days. |
| | **E1‑S4** As a developer, I want to logout, so that the user’s session is invalidated. | • POST `/api/auth/logout` revokes refresh token. <br>• Subsequent refresh attempts fail. |
| | **E1‑S5** As a developer, I want to protect routes with a middleware, so that only authenticated users can access them. | • Middleware validates JWT, attaches `req.user`. <br>• 401 on missing/invalid token. |
| **License Management** | **E2‑S1** As a developer, I want to generate a license key for a user, so that I can restrict feature access. | • POST `/api/license/generate` with `userId`, `plan`, `expiry`. <br>• Returns a signed license string (JWT). <br>• License contains `userId`, `plan`, `expiresAt`. |
| | **E2‑S2** As a developer, I want to validate a license key client‑side, so that the app can enable/disable features. | • Client calls `/api/license/validate` with key. <br>• Returns license payload or 400 if invalid/expired. |
| | **E2‑S3** As a developer, I want to revoke a license, so that I can disable a user’s access. | • DELETE `/api/license/revoke` with `licenseId`. <br>• Subsequent validations fail. |
| | **E2‑S4** As a developer, I want to list all licenses for a user, so that I can audit usage. | • GET `/api/license/user/:userId` returns paginated list. |
| **Security & Compliance** | **E3‑S1** As a developer, I want to enforce HTTPS, so that data is encrypted in transit. | • All endpoints require TLS. <br>• 301 redirect from HTTP to HTTPS. |
| | **E3‑S2** As a developer, I want to store secrets in environment variables, so that I avoid hard‑coding. | • No secrets in repo. <br>• `.env.example` provided. |
| | **E3‑S3** As a developer, I want to log authentication events, so that I can audit security incidents. | • Logs include timestamp, IP, action, status. <br>• Stored in rotating log files. |
| **Developer Experience** | **E4‑S1** As a developer, I want a Docker image, so that I can spin up the service quickly. | • `Dockerfile` builds image. <br>• `docker-compose.yml` sets up DB, Redis, API. |
| | **E4‑S2** As a developer, I want a CLI tool, so that I can generate licenses locally. | • `auth-licence-cli` accepts `--user`, `--plan`, `--expiry`. <br>• Prints signed license. |
| | **E4‑S3** As a developer, I want comprehensive docs, so that I can integrate without confusion. | • README includes installation, usage, API reference. <br>• Example code snippets in JavaScript/Node. |
| **Monitoring & Alerts** | **E5‑S1** As a developer, I want to expose Prometheus metrics, so that I can monitor health. | • `/metrics` endpoint exposes request counts, latency, error rates. |
| | **E5‑S2** As a developer, I want email alerts on license revocation, so that I stay informed. | • Configurable email webhook on revoke event. |

---

## MVP Order (by priority)

1. **Core Authentication** (E1‑S1 to S5) – foundational user flow.  
2. **License Generation & Validation** (E2‑S1 to S2) – core product value.  
3. **License Revocation & Listing** (E2‑S3, S4) – admin controls.  
4. **Security & Compliance** (E3‑S1 to S3) – mandatory for production.  
5. **Developer Experience** (E4‑S1 to S3) – ease of adoption.  
6. **Monitoring & Alerts** (E5‑S1 to S2) – operational excellence.

---

## Notes & Constraints

- **Tech Stack**: Node.js (Express), PostgreSQL, Redis (for token store), JWT for auth & license.  
- **License Format**: Signed JWT with HS256; payload: `{ userId, plan, expiresAt }`.  
- **Rate limiting**: Implement via Redis.  
- **Testing**: Unit tests (Jest) + integration tests (Supertest).  
- **CI/CD**: GitHub Actions – lint, test, build Docker, push to registry.  

---
