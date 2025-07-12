# Compliance Guardrails

Aegis Health aims to comply with HIPAA (US) and GDPR (EU) requirements for the handling of personal and health information. This document enumerates the safeguards built into the platform and areas requiring future work.

## HIPAA

| HIPAA Rule | Guardrail | Implementation |
| --- | --- | --- |
| **Privacy Rule** | Limit PHI use and disclosure | Pseudonymous identifiers; per‑tenant isolation; consent flags |
| **Security Rule** | Ensure confidentiality, integrity and availability | Encryption at rest/in transit; RBAC; monitoring; backups |
| **Breach Notification Rule** | Notify affected parties within 60 days | Incident response plan with notification templates (see `RUNBOOKS.md`) |

## GDPR

| GDPR Article | Requirement | Implementation |
| --- | --- | --- |
| **Art. 5** | Data minimisation | Collect only logs and wearable metrics necessary for predictions |
| **Art. 6** | Lawful basis | Obtain explicit consent from users during onboarding |
| **Art. 17** | Right to erasure | `/v1/data/delete` endpoint deletes all user data; scheduled background jobs ensure complete removal |
| **Art. 20** | Data portability | `/v1/data/export` endpoint returns encrypted archive of user records |
| **Art. 25** | Privacy by design | Security baked into architecture; pseudonymous IDs; encrypted logs |
| **Art. 32** | Security of processing | See `SECURITY_PRIVACY.md`; continuous vulnerability scanning and patching |

## Additional Guardrails

* **Third‑Party Agreements:** We execute Business Associate Agreements (BAAs) with vendors (e.g., Auth0, GCP) who handle PHI.  
* **Training:** All engineers must complete annual HIPAA/GDPR training.  
* **Access Reviews:** Quarterly audits of IAM roles and group memberships.  
* **Data Localization:** For EU customers, data is stored in European regions; this is configurable via Terraform variables.

## Open Items

| Item | Owner | Due |
| --- | --- | --- |
| Publish Data Protection Impact Assessment | Compliance lead | 2025‑09‑01 |
| Evaluate HIPAA audit logging tools | DevOps | 2025‑09‑15 |
| Implement Data Protection Officer contact channel | Legal | 2025‑08‑20 |
