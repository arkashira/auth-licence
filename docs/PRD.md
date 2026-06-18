# Product Requirements Document – auth‑licence

---

## 1. Problem Statement  

Solo founders and small SaaS developers often ship web applications without a robust, developer‑friendly authentication and licensing layer.  
- **Piracy risk**: Unprotected APIs and web UIs are easy targets for reverse‑engineering and unauthorized distribution.  
- **High friction**: Existing solutions (e.g., Auth0, Firebase, custom JWT stacks) require significant integration effort, configuration, and ongoing maintenance.  
- **Cost & complexity**: Many SaaS founders cannot afford enterprise‑grade licensing services or the engineering time to build their own.  

Result: **Revenue leakage** and **security gaps** that erode trust and growth potential.

---

## 2. Target Users  

| Persona | Pain Points | Desired Outcomes |
|---------|-------------|------------------|
| **Solo Founder / Indie Dev** | Limited engineering bandwidth, tight budget, need quick launch | One‑click auth/licensing, minimal code changes, low cost |
| **Small SaaS Team (≤10 devs)** | Need to protect API keys, enforce trial periods, manage subscription tiers | Scalable, API‑first licensing, easy admin UI |
| **Product Managers** | Track usage, enforce compliance, reduce support tickets | Clear usage metrics, audit logs, automated license revocation |

---

## 3. Goals & Success Metrics  

| Goal | Success Metric | Target |
|------|----------------|--------|
| **Reduce piracy incidents** | % of unauthorized deployments detected | < 5% of total deployments |
| **Lower integration time** | Avg. time from repo clone to production‑ready auth | < 30 min |
| **Improve developer satisfaction** | NPS score for auth‑licence | ≥ 70 |
| **Drive revenue** | % of users who upgrade to paid tier | ≥ 15% of free users |
| **Maintain high uptime** | Service availability | 99.9% |

---

## 4. Key Features (Prioritized)

| # | Feature | Description | Priority |
|---|---------|-------------|----------|
| 1 | **Zero‑config JWT & API Key auth** | Auto‑generate JWT tokens and API keys on first run; no external dependencies. | Must‑Have |
| 2 | **License Key Generation & Validation** | One‑time license keys with embedded metadata (expiry, feature flags). | Must‑Have |
| 3 | **Trial & Subscription Management** | Built‑in trial period, auto‑downgrade, and webhook hooks for billing services. | Must‑Have |
| 4 | **Admin Dashboard** | Lightweight UI for managing users, licenses, and audit logs. | Nice‑to‑Have |
| 5 | **SDKs (Node, Python, Go)** | Ready‑to‑use libraries for common stacks. | Nice‑to‑Have |
| 6 | **Rate‑Limiting & Abuse Detection** | Basic throttling and anomaly alerts. | Nice‑to‑Have |
| 7 | **Self‑hosted & Cloud‑managed Options** | Docker image + Helm chart; optional SaaS‑hosted instance. | Nice‑to‑Have |
| 8 | **Compliance & GDPR** | Data minimization, export, and deletion capabilities. | Nice‑to‑Have |
| 9 | **Marketplace Integration** | Easy plug‑in for Stripe, Paddle, or custom payment gateways. | Nice‑to‑Have |
|10 | **Documentation & Tutorials** | Step‑by‑step guides, code samples, and video walkthroughs. | Must‑Have |

---

## 5. Scope

| Item | In‑Scope | Out‑of‑Scope |
|------|----------|--------------|
| **Core Auth** | JWT, API key, OAuth2 (basic) | Full OAuth2 provider, SSO |
| **Licensing** | License key generation, validation, revocation | Enterprise license tiers, multi‑tenant licensing |
| **Billing Hooks** | Webhooks for Stripe, Paddle | Full billing UI |
| **Admin UI** | Lightweight dashboard | Full‑blown SaaS admin portal |
| **SDKs** | Node, Python, Go | Rust, Ruby, PHP |
| **Deployment** | Docker, Helm | Kubernetes Operators |
| **Compliance** | GDPR data export | PCI‑DSS compliance |

---

## 6. Deliverables

1. **Auth‑licence Core Library** – Go‑based, open‑source, MIT licensed.  
2. **SDKs** – Node, Python, Go.  
3. **Admin Dashboard** – React + Vite, hosted on Netlify.  
4. **Docker Image** – `auth-licence:latest`.  
5. **Documentation** – Markdown + video tutorials.  
6. **CI/CD Pipeline** – GitHub Actions with automated tests, linting, and release tagging.  

---

## 7. Technical Constraints

- **Language**: Go for core, SDKs in target languages.  
- **Database**: PostgreSQL (self‑hosted) or SQLite for single‑user dev.  
- **Security**: TLS‑only endpoints, hashed secrets, HSM‑grade key rotation.  
- **Scalability**: Stateless API, horizontal scaling via Kubernetes.  

---

## 8. Timeline (High‑Level)

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Discovery & Design | 2 weeks | PRD final, architecture diagram |
| Core Library MVP | 4 weeks | JWT + API key auth, license key generation |
| SDKs & Docs | 3 weeks | Node, Python, Go SDKs, docs |
| Admin Dashboard | 3 weeks | Basic UI, CRUD ops |
| Beta Release | 2 weeks | Public beta, feedback loop |
| Public Launch | 1 week | Version 1.0, marketing assets |

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Security Breach** | High | Code audit, dependency scanning, rate limiting |
| **Low Adoption** | Medium | Community outreach, GitHub stars, early adopter program |
| **License Key Abuse** | Medium | Rate limiting, anomaly detection, revocation API |
| **Compliance Issues** | Low | GDPR‑ready data handling, clear privacy policy |

---

## 10. Stakeholders

- **Product**: Lead, PM, UX designer  
- **Engineering**: Core devs, QA, DevOps  
- **Marketing**: Community manager, content writer  
- **Legal**: Compliance officer, privacy specialist  

---

## 11. Dependencies

- PostgreSQL (or SQLite)  
- Docker & Helm for deployment  
- Stripe/Paddle SDKs for billing hooks  
- Vercel/Netlify for dashboard hosting  

---

## 12. Acceptance Criteria

1. **Auth Flow** – Developers can integrate with a single line of code and have authenticated endpoints.  
2. **License Validation** – License keys are validated within 50 ms, with clear error messages.  
3. **Admin UI** – CRUD operations for users, licenses, and logs.  
4. **Documentation** – Complete, example‑driven, and passes peer review.  
5. **Performance** – 99.9% uptime in CI, 200 ms average response time.  

---

### Appendix

- **Glossary**  
  - *License Key*: One‑time code granting access to features.  
  - *Trial*: Time‑bound free access.  
  - *Webhook*: HTTP callback for billing events.  

- **References**  
  - [Auth‑licence GitHub Repo](https://github.com/arkashira/auth-licence)  
  - [Axentx Runbook](https://github.com/arkashira/surrogate-1-harvest)  

---
