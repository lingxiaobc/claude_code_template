# Security and Auth

Use this file whenever an API touches protected data, users, organizations, tenants, files, money, external services, or side effects.

## Auth Grounding

Do not invent auth behavior.

Find existing:

- Auth middleware, guard, dependency, decorator, or filter
- Current-user/session extraction
- Role or permission model
- Tenant or organization scoping
- Ownership checks
- Test helpers for authenticated users

If no auth exists and the endpoint writes or exposes sensitive data, ask the user whether it should be public.

## Authorization

Separate authentication from authorization:

- Authentication: who is making the request?
- Authorization: are they allowed to perform this action on this resource?

Confirm whether the rule depends on:

- Role
- Permission
- Ownership
- Organization or tenant membership
- Resource status
- Feature flag
- Subscription or billing state
- Admin override

Do not replace existing policy systems with inline checks unless nearby code does that.

## Input Safety

Validate and normalize:

- IDs
- Dates
- Pagination limits
- Sort keys
- Filter fields
- File names and MIME types
- URLs
- Webhook signatures and payloads

Use allowlists for sort and filter fields. Do not pass user-controlled field names directly into queries.

## Sensitive Data

Do not expose:

- Password hashes
- Tokens
- API keys
- Secrets
- Internal IDs if the project hides them
- Internal error messages
- Stack traces
- Private user data not required by the client

Do not log secrets, tokens, full authorization headers, or sensitive request bodies.

## Database Safety

Avoid:

- SQL string interpolation
- Unbounded list queries
- Unchecked bulk updates or deletes
- Missing tenant filters
- Missing ownership filters
- Returning deleted or archived records unless intended

For destructive actions, confirm whether soft delete is the project convention.

## External Calls and Webhooks

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

For uploads or file references:

- Validate size and content type.
- Avoid trusting client-provided file names.
- Avoid path traversal.
- Store metadata consistently.
- Confirm access control for downloads.
