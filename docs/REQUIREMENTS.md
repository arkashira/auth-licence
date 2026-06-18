# REQUIREMENTS.md

## Project: auth‑licence  
**Repository:** `auth-licence`  
**Owner:** Axentx  
**Purpose:** Provide a lightweight, easy‑to‑integrate authentication and licensing solution for solo founders and small SaaS developers to protect their web applications from piracy.

---

## 1. Functional Requirements

| ID | Description | Priority | Notes |
|----|-------------|----------|-------|
| **FR‑1** | **User Registration** – Allow new users to create an account with email/password or OAuth (Google, GitHub). | Must | Store hashed passwords (bcrypt) and OAuth tokens. |
| **FR‑2** | **Login & Session Management** – Issue JWTs with configurable expiration; support refresh tokens. | Must | JWTs signed with RS256; refresh tokens stored in DB with revocation list. |
| **FR‑3** | **License Generation** – Generate a unique license key per user per product, optionally with expiration and feature flags. | Must | Keys are deterministic (HMAC‑SHA256) and stored in DB. |
| **FR‑4** | **License Validation API** – Expose a `/validate` endpoint that accepts a license key and returns product access status. | Must | Must support CDN caching and rate limiting. |
| **FR‑5** | **License Revocation** – Admin UI/API to revoke or suspend licenses. | Must | Revocation stored in DB; immediate effect on next validation. |
| **FR‑6** | **Audit Logging** – Log all registration, login, license issuance, validation, and revocation events. | Must | Logs stored in structured JSON, rotated daily. |
| **FR‑7** | **Admin Dashboard** – Web UI for managing users, licenses, and viewing audit logs. | Should | Built with React, protected by admin role. |
| **FR‑8** | **Self‑Service License Renewal** – Allow users to renew expiring licenses via email link. | Should | Email template stored in DB; link contains signed token. |
| **FR‑9** | **Multi‑Tenant Support** – Separate data isolation per SaaS product owner. | Should | All tables partitioned by `tenant_id`. |
| **FR‑10** | **SDKs** – Provide Node.js and Python SDKs for easy integration. | Should | SDKs expose `authenticate`, `validateLicense`, `renewLicense`. |

---

## 2. Non‑Functional Requirements

| Category | Requirement | Target |
|----------|-------------|--------|
| **Performance** | API response time < 200 ms for 95 % of requests. | 200 ms |
| **Scalability** | Handle 10k concurrent validation requests with 99.9 % uptime. | 10k |
| **Security** | • All traffic over TLS 1.3.<br>• JWT secrets rotated every 90 days.<br>• Passwords stored with bcrypt (cost 12).<br>• Rate limit 100 requests/min per IP for validation endpoint. | 1.3, 90 days, 12, 100 |
| **Reliability** | 99.95 % uptime SLA for API. | 99.95 % |
| **Data Integrity** | ACID compliance for license issuance and revocation. | ACID |
| **Compliance** | GDPR‑compliant data handling; provide data export and deletion on request. | GDPR |
| **Observability** | Metrics (latency, error rate, request count) exposed via Prometheus; logs shipped to ELK stack. | Prometheus, ELK |
| **Maintainability** | Codebase follows SOLID principles; unit test coverage ≥ 80 %. | SOLID, 80 % |

---

## 3. Constraints

1. **Technology Stack** – Must use the existing Axentx tech stack:  
   - Backend: FastAPI (Python 3.12)  
   - Database: PostgreSQL 16 (with JSONB support)  
   - Messaging: Redis for rate limiting and cache  
   - Deployment: Docker Compose for dev, Kubernetes for prod  
2. **License Key Format** – 32‑character alphanumeric, case‑insensitive, checksum included.  
3. **Third‑Party Services** – Email via SendGrid; OAuth via Google/GitHub only.  
4. **Licensing** – Must comply with open‑source licenses of all dependencies (MIT, Apache‑2.0).  
5. **Deployment** – Must run on AWS Fargate with IAM roles for secrets.  
6. **Data Residency** – All user data must reside in EU‑West‑1 region.  

---

## 4. Assumptions

- Users will integrate via provided SDKs or direct REST calls.  
- The SaaS product owner will supply a `product_id` when creating licenses.  
- The system will operate in a single‑region deployment; cross‑region failover is out of scope.  
- All external services (SendGrid, OAuth providers) are available and functional.  
- The admin dashboard will be accessed only by authenticated admin users.  

---

## 5. Deliverables

1. **API Specification** – OpenAPI v3 document covering all endpoints.  
2. **Database Schema** – ER diagram and migration scripts.  
3. **SDK Packages** – Published to PyPI and npm.  
4. **Admin Dashboard** – React SPA with authentication.  
5. **Testing Suite** – Unit, integration, and load tests.  
6. **Documentation** – Setup guide, developer guide, and user guide.  

---

## 6. Acceptance Criteria

- All functional requirements are implemented and pass unit tests.  
- API meets performance targets under load test (10k concurrent validations).  
- Security audit confirms no OWASP Top 10 vulnerabilities.  
- GDPR compliance checklist is satisfied.  
- Documentation is complete and reviewed by the product team.  

---
