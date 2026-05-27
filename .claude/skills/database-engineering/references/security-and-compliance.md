# Security and Compliance

Use this whenever data includes users, tenants, permissions, PII, secrets, payments, audit logs, retention, or deletion requirements.

## Sensitive Data

Classify fields:

- Public
- Internal
- Personal data
- Confidential business data
- Secret credential
- Payment or financial data
- Regulated data

For sensitive fields, define:

- Whether it should be stored at all
- Encryption or hashing strategy
- Redaction in logs and exports
- Access control
- Retention and deletion behavior
- Audit requirements

Passwords must be hashed with a password hashing algorithm. Never store plaintext passwords.

## Tenant Isolation

For multi-tenant systems:

- Include tenant scope on tenant-owned tables
- Include tenant filters in every query path
- Include tenant scope in unique constraints
- Test cross-tenant access attempts
- Avoid global IDs that bypass tenant checks unless authorization is explicit

Missing tenant scope is a data breach risk, not just a bug.

## Authorization Fields

Model ownership explicitly:

- `user_id`
- `organization_id`
- `workspace_id`
- `team_id`
- role or membership table
- permission grants

Do not infer ownership from display-only fields.

## Audit

For important changes, capture:

- Actor
- Action
- Target record
- Timestamp
- Previous and new value when required
- Request or correlation ID when available

Use append-only audit/event tables for high-integrity histories.

## Deletion and Retention

Decide per entity:

- Hard delete
- Soft delete
- Archive
- Anonymize
- Legal hold
- Retain forever

Financial, payment, audit, and compliance records often must not be hard-deleted.

## Injection Safety

Avoid:

- String concatenation in SQL
- User-controlled column names or sort fields without allowlists
- User-controlled table names
- Raw JSON path or SQL fragments from requests

Use parameters for values and allowlists for identifiers.

## Backups and Restore

For critical systems, ask whether the design needs:

- Backup retention
- Point-in-time recovery
- Restore drills
- Disaster recovery target
- Data export
- Data residency

Schema design should not assume backups solve all data integrity problems.
