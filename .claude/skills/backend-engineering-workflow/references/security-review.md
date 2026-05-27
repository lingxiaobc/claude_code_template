# Security Review

Use this whenever the backend touches protected data, users, tenants, auth, files, payments, external services, or side effects.

## Auth Grounding

Find existing:

- Auth middleware, guard, dependency, decorator, or filter
- Current-user/session extraction
- Role or permission model
- Tenant or organization scoping
- Ownership checks
- Test helpers for authenticated requests

Do not invent auth rules.

## Authorization

Confirm whether permissions depend on:

- Role
- Permission
- Ownership
- Organization or tenant membership
- Resource status
- Feature flag
- Subscription or billing state
- Admin override

Authentication answers who the user is. Authorization answers what they may do.

## Input Safety

Validate and allowlist:

- IDs
- Dates
- Sort fields
- Filter fields
- File names and MIME types
- URLs
- Webhook signatures

Do not pass user-controlled field names directly into queries.

## Sensitive Data

Do not expose or log:

- Password hashes
- Tokens
- API keys
- Secrets
- Full authorization headers
- Stack traces
- Internal provider errors
- Private data not required by the client

## Common Risk Areas

Check:

- SQL injection
- SSRF through user-controlled URLs
- Path traversal
- Unsafe file upload/download
- Wildcard CORS on protected APIs
- Missing tenant filters
- Missing ownership checks
- Missing rate limit on sensitive endpoints
- Webhooks without signature validation
- Disabled TLS verification

Use `scripts/scan_backend_risks.py` for a first-pass static scan, then review findings manually.
