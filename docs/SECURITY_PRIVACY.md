# Security & Privacy Practices

The protection of user data—particularly protected health information (PHI)—is central to Aegis Health. We adhere to industry best practices and regulatory requirements throughout the development and operation of the system.

## Threat Model

We employ the STRIDE model to identify potential threats:

| Category | Threat | Mitigation |
| --- | --- | --- |
| **Spoofing** | Attacker pretends to be a legitimate user | OAuth2/OIDC flows with PKCE, multi‑factor authentication; short‑lived access tokens |
| **Tampering** | Altering data in transit or storage | TLS 1.3 for all network communication; AES‑256 encryption at rest (Cloud SQL, GCS); signed tokens |
| **Repudiation** | Users deny actions | Audit logs for all API calls and data mutations; immutable logs stored in BigQuery |
| **Information Disclosure** | Unauthorised access to PHI | RBAC enforced in API; per‑tenant isolation; minimal privilege IAM roles |
| **Denial of Service** | Overloading services to degrade performance | Rate limiting (FastAPI throttling); autoscaling of Cloud Run services; load tests to set SLO budgets |
| **Elevation of Privilege** | Gaining higher privileges | Principle of least privilege; no default admin accounts; mandatory access reviews |

## Authentication & Authorisation

* **Auth0** provides OAuth2 flows with PKCE for both clients. Users authenticate via biometric or password on mobile and via browser for web.
* The API validates JWTs and checks scopes/roles. Roles include `patient`, `clinician` and `admin`.
* Sensitive endpoints (e.g., deletion/export) require elevated scopes and additional confirmation.

## Encryption

* **At rest:** All databases (Postgres), storage buckets (GCS) and backups use AES‑256 encryption. Terraform enforces encryption settings and disables public access.
* **In transit:** TLS certificates are automatically provisioned via GCP’s managed SSL for Cloud Run. All HTTP endpoints redirect to HTTPS.

## Secret Management

* Secrets (database passwords, Auth0 client IDs) live in **GCP Secret Manager**.  
* Locally, secrets are loaded from a `.env` file not checked into version control. `Makefile` tasks fail if `.env` is missing.

## Auditing & Logging

* All API requests and model inferences are logged with user ID, tenant ID, request parameters (redacted where necessary), status code and latency.  
* Logs are shipped to BigQuery via Cloud Logging sinks and retained for 2 years.  
* Access to audit logs is restricted and monitored.

## Vulnerability Management

* Dependabot monitors dependencies in GitHub. Critical CVEs are patched promptly.  
* CI pipeline runs static analysis (Bandit for Python, npm audit) on each pull request.  
* Infrastructure is scanned via Terraform’s built‑in validators and third‑party tools.

## Incident Response

* On‑call engineers follow procedures defined in `docs/RUNBOOKS.md`.  
* Incident severity levels and escalation paths are documented.  
* Post‑mortems are held for any security incident with action items captured in the roadmap.
