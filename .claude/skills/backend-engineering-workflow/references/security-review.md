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

## Database Safety

Avoid:

- SQL string interpolation
- Unbounded list queries
- Unchecked bulk updates or deletes
- Missing tenant filters
- Missing ownership filters
- Returning deleted or archived records unless intended

For destructive actions, confirm whether soft delete is the project convention.

## External Calls And Webhooks

For external API calls:

- Use configured clients and timeouts.
- Handle errors explicitly.
- Avoid leaking external provider errors directly to users.
- Mock external calls in tests where appropriate.

For webhooks:

- Verify signatures if the provider supports them.
- Reject stale timestamps when the project does so.
- Make handlers idempotent when retries are possible.

## Files

For uploads, downloads, or file references:

- Validate size and content type.
- Avoid trusting client-provided file names.
- Avoid path traversal.
- Store metadata consistently.
- Confirm access control for downloads.

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
