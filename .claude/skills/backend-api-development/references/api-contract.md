# API Contract

Use this file before implementing or modifying an endpoint.

## Contract Template

Define this contract for each endpoint, resolver, or RPC method:

```text
Name:
Method and path, resolver, or RPC name:
Purpose:
Auth required:
Permission rule:
Path params:
Query params:
Request body:
Validation:
Success status:
Success response:
Error responses:
Database reads:
Database writes:
External side effects:
Pagination/filtering/sorting:
Idempotency:
Backward compatibility:
Documentation updates:
Tests:
```

Keep the contract short but concrete. It is a working target, not a design document.

## Fact Sources

Use these sources in order:

1. Existing endpoint code for the same resource
2. Existing tests
3. Database schema, ORM model, or migration
4. API docs, OpenAPI spec, GraphQL schema, or typed client
5. Product requirements from the user
6. Direct user confirmation

Do not infer sensitive facts such as roles, permissions, tenant boundaries, billing rules, inventory rules, or data retention behavior.

## Request Design

For request fields:

- Confirm names and types from existing models or requirements.
- Define required vs optional.
- Define defaults.
- Define string trimming and normalization rules.
- Define enum values from schema or existing code.
- Define numeric ranges and date/time handling.
- Define unknown-field behavior if the project has a pattern.

For query params:

- Match existing pagination names such as `page`, `limit`, `offset`, `cursor`, `take`, `skip`.
- Match existing sorting and filtering conventions.
- Confirm max limits and defaults.

## Response Design

Match existing response shape:

- Envelope vs raw object
- `data` wrapper
- `meta` wrapper
- Error object shape
- Date serialization
- ID format
- Null vs omitted fields
- Pagination metadata

Avoid adding fields that clients do not need. Avoid breaking existing fields unless the user explicitly requested a breaking change.

## Error Contract

Define expected behavior for:

- Invalid request body
- Invalid query or path param
- Unauthenticated request
- Authenticated but forbidden request
- Resource not found
- Conflict or uniqueness violation
- External service failure
- Rate limit or quota failure if relevant

Use the project's existing error helpers and status-code conventions.

## Side Effects

Call out:

- Database writes
- Audit logs
- Emails
- Webhooks
- Queue jobs
- File uploads or deletion
- Cache invalidation
- External API calls

For side effects, consider idempotency, transactions, retries, timeouts, and whether tests should mock external services.
