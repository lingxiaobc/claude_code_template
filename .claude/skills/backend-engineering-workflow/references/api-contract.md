# API Contract

Use this before implementing or changing an API, resolver, RPC method, webhook, or public service behavior.

## Template

```text
Name:
Purpose:
Method/path or resolver/RPC name:
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

## Fact Sources

Use these sources in order:

1. Existing endpoint code
2. Existing tests
3. Models, ORM schemas, migrations, generated types
4. OpenAPI, GraphQL schema, typed client, or API docs
5. User requirements
6. Direct user confirmation

Do not invent fields, roles, tenant boundaries, status codes, or response wrappers.

## Request Rules

Define:

- Required and optional fields
- Defaults
- Normalization such as trimming or lowercasing
- Enum values
- Numeric limits
- Date/time format
- Unknown field behavior
- Pagination defaults and maximums
- Allowed filter and sort fields

## Response Rules

Match project conventions:

- Raw object or `data` wrapper
- `meta` wrapper
- Error object shape
- Date serialization
- ID format
- Null vs omitted fields
- Pagination metadata

Avoid changing existing response semantics unless requested.

## Errors

Define expected behavior for:

- Invalid input
- Unauthenticated request
- Forbidden request
- Not found
- Conflict
- External dependency failure
- Rate or quota failure

Use existing error helpers and status-code conventions.

## Side Effects

Call out:

- Database writes
- Queue jobs
- Emails
- Webhooks
- Audit logs
- File operations
- Cache invalidation
- External API calls

For side effects, consider transactions, retries, timeouts, and idempotency.
