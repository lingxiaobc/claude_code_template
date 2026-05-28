# API Development

Use this reference for endpoint-focused backend work: REST routes, GraphQL resolvers, RPC handlers, controllers, request/response schemas, OpenAPI/Swagger updates, and HTTP smoke checks.

## Phase Mapping

For API-only tasks, apply the main workflow with this emphasis:

1. Inspect endpoint, auth, validation, data, error, docs, and test patterns.
2. Define the endpoint contract before coding.
3. Choose the smallest file set that fits the local architecture.
4. Implement against local route/controller/service/repository patterns.
5. Verify static checks, route behavior, auth behavior, errors, docs, and side effects.

## Inspect Checklist

Find facts before editing:

- Runtime, framework, package manager, and scripts
- Existing route, controller, resolver, or RPC style
- Service, repository, model, schema, and migration locations
- Validation and serialization patterns
- Auth, permission, tenant, and session handling
- Error response shape and status-code conventions
- Tests near similar endpoints
- OpenAPI, Swagger, GraphQL schema, RPC schema, or typed client generation

Do not guess framework, ORM, route layout, auth system, validation library, or test command. If a required fact cannot be found locally and a conservative assumption would affect data, security, or client compatibility, ask the user before implementing.

## Contract Checklist

Define the contract for each endpoint, resolver, or RPC method:

- Method and path, resolver name, or RPC name
- Authentication and authorization
- Path params, query params, and request body
- Validation rules, defaults, and normalization
- Success response body and status code
- Error responses and status codes
- Database reads and writes
- External side effects
- Pagination, filtering, sorting, and idempotency
- Backward compatibility concerns
- Documentation and generated-client updates
- Tests required

Do not invent database fields, enum values, roles, tenant rules, or response formats. Confirm them from schemas, models, migrations, existing endpoints, API docs, or the user.

## Implementation Notes

Prefer existing project patterns:

- Existing controller/service/repository boundaries
- Existing validators, DTOs, serializers, schemas, and error helpers
- Existing auth guards, middleware, policies, decorators, and permission checks
- Existing pagination, filtering, sorting, and response wrappers
- Existing API documentation and generated-client workflow
- Existing test style, fixtures, factories, and authenticated-request helpers

Keep business logic out of route glue when the project has service or use-case layers. Validate every user-controlled input. Preserve backward compatibility unless the user requested a breaking change. Use transactions for multi-step writes that must succeed or fail together. Avoid raw SQL string interpolation. Avoid leaking stack traces, secrets, tokens, provider errors, or internal details to clients.

## Verification Notes

For new or changed endpoints, cover:

- Happy path
- Invalid body, path param, or query param
- Unauthenticated request when auth applies
- Authenticated but forbidden request when permissions apply
- Not found
- Conflict or uniqueness issue when relevant
- Pagination, filtering, and sorting behavior when relevant
- Database write side effects
- External service failure with mocks when relevant

When a local server can run, perform HTTP verification:

1. Start the server with the repo's script.
2. Exercise at least one happy path.
3. Exercise at least one validation or error path.
4. Exercise unauthenticated or unauthorized behavior when auth applies.
5. Inspect status, headers, and response body.
6. Confirm database state for write endpoints when practical.

Use `scripts/verify_api.py` for generic HTTP smoke checks. Use project-native integration tests or custom Playwright/API automation for setup-heavy auth or data flows.
