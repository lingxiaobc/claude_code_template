# Verification Checklist

Use this file during the Verify phase.

## Static Checks

Use project-native commands:

- Type check or compile
- Lint
- Format check
- Unit tests
- Integration tests
- Build
- OpenAPI/GraphQL/schema generation

Read scripts before running commands. Prefer the repo's existing commands over generic guesses.

## Test Coverage

For new or changed endpoints, cover:

- Happy path
- Invalid request body
- Invalid path/query parameter
- Unauthenticated request if auth applies
- Authenticated but forbidden request if permissions apply
- Resource not found
- Conflict or uniqueness issue when relevant
- Pagination/filter/sort behavior when relevant
- Database write side effects
- External service failure when relevant

If the project has no test infrastructure, use HTTP smoke checks and report the gap.

## HTTP Smoke Checks

When the server can run locally:

1. Start the server with the repo's dev/test script.
2. Exercise the happy path.
3. Exercise at least one error path.
4. Exercise unauthenticated or unauthorized behavior when auth applies.
5. Inspect response status, headers, and body.
6. Confirm database state for write endpoints when practical.

Use `scripts/verify_api.py` for generic checks. Use custom scripts or project tests for deeper setup and auth flows.

## API Documentation Checks

If the project has API docs:

- Confirm OpenAPI/Swagger generation succeeds.
- Confirm documented request and response match implementation.
- Confirm GraphQL schema generation succeeds.
- Confirm typed client generation succeeds if present.

## Performance Checks

For optimization tasks:

- Reproduce or identify the bottleneck.
- Measure before and after if the environment supports it.
- Add a regression test or benchmark when practical.
- Confirm response contract is unchanged unless intentionally changed.

## Completion Bar

Do not declare success until:

- Relevant static checks ran or limitations are reported.
- Relevant tests ran or limitations are reported.
- Route-level behavior was verified.
- Auth and permission behavior were checked when applicable.
- Error behavior was checked.
- Known risks are explicitly stated.
