---
name: backend-api-development
description: "End-to-end backend API development workflow for creating, modifying, optimizing, debugging, testing, and documenting server endpoints. Use when the user asks to build or adjust REST APIs, GraphQL resolvers, RPC handlers, controllers, routes, request validation, response schemas, authentication, authorization, pagination, filtering, sorting, OpenAPI/Swagger specs, backend integration tests, or API performance/error handling. The workflow requires project inspection, API contract planning, scoped implementation, and verification. Do NOT use for frontend-only work, database-only analysis with no API change, deployment-only tasks, or high-level architecture discussion with no implementation."
---

# Backend API Development

Use this skill to build, optimize, or adjust backend interfaces through five phases:

1. Inspect
2. Contract
3. Orchestrate
4. Implement
5. Verify

Backend API work affects data, security, permissions, and client contracts. Reduce hallucination by grounding every implementation choice in project files, schemas, existing endpoint patterns, or explicit user confirmation.

## Resource Guide

Load these files only when needed:

- `references/project-recon.md`: Use during Inspect to identify framework, commands, routes, tests, database, and auth patterns.
- `references/api-contract.md`: Use during Contract to define method, path, auth, request, response, errors, side effects, and tests before coding.
- `references/implementation-patterns.md`: Use during Implement for controller/service/repository layering, validation, errors, docs, and optimization.
- `references/security-and-auth.md`: Use whenever an endpoint reads or writes protected data, touches users, roles, sessions, tokens, files, webhooks, or external services.
- `references/database-and-migrations.md`: Use whenever the work depends on models, ORM schemas, migrations, indexes, transactions, or data shape.
- `references/verification-checklist.md`: Use during Verify for static checks, unit/integration tests, HTTP smoke checks, and completion criteria.
- `scripts/inspect_backend.py`: Use as a black-box project reconnaissance helper. Run `python scripts/inspect_backend.py --help` before using it.
- `scripts/verify_api.py`: Use as a black-box HTTP smoke-test helper. Run `python scripts/verify_api.py --help` before using it.

## Phase 1: Inspect

Inspect before editing. Do not guess the framework, ORM, route layout, auth system, validation library, or test command.

Find:

- Runtime and framework
- Package manager and scripts
- Existing route/controller/resolver style
- Service, repository, model, schema, and migration locations
- Validation and serialization patterns
- Auth, permission, tenant, and session handling
- Error response shape
- Existing tests near similar endpoints
- OpenAPI, Swagger, GraphQL schema, or typed client generation

Use `scripts/inspect_backend.py` for a first pass, then read the relevant files it identifies. For detailed recon guidance, read `references/project-recon.md`.

If a required fact cannot be found locally and a conservative assumption would affect data, security, or client compatibility, ask the user before implementing.

## Phase 2: Contract

Define the API contract before coding.

For each endpoint or resolver, identify:

- Method and path, or resolver/RPC name
- Authentication and authorization
- Path params, query params, and request body
- Validation rules and defaults
- Success response body and status code
- Error responses and status codes
- Database reads and writes
- External side effects
- Pagination, filtering, sorting, and idempotency
- Backward compatibility concerns
- Tests required

Do not invent database fields, enum values, roles, tenant rules, or response formats. Confirm them from schemas, models, migrations, existing endpoints, API docs, or the user.

For detailed contract guidance, read `references/api-contract.md`.

## Phase 3: Orchestrate

Choose the smallest implementation path that fits the project.

Prefer:

- Existing endpoint patterns
- Existing controller/service/repository boundaries
- Existing validators, DTOs, serializers, schemas, and error helpers
- Existing auth guards, middleware, policies, decorators, and permission checks
- Existing test style and fixtures

Before editing substantial code, determine the likely file set:

1. Route/controller/resolver
2. Request/response schema or DTO
3. Service or use-case logic
4. Repository or database access
5. Migration/model changes if needed
6. API documentation or generated client if the project maintains it
7. Unit or integration tests

Avoid broad refactors and new dependencies unless the user asked for them or the repo already uses that dependency.

## Phase 4: Implement

Implement against the contract and local patterns.

Rules:

- Reuse existing framework APIs and patterns from nearby code.
- Keep business logic out of route glue when the project has service/use-case layers.
- Validate all user-controlled inputs.
- Return errors in the project's existing error shape.
- Preserve backward compatibility unless the user asked for a breaking change.
- Use transactions for multi-step writes that must succeed or fail together.
- Avoid raw SQL string interpolation.
- Avoid leaking stack traces, secrets, tokens, or internal details to clients.
- Do not silently skip auth or permission checks to make tests pass.
- Add or update focused tests when the repo has a test path.

For detailed implementation guidance, read:

- `references/implementation-patterns.md`
- `references/security-and-auth.md`
- `references/database-and-migrations.md`

## Phase 5: Verify

Do not finish after writing code. Verify with the strongest checks the environment supports.

Run relevant static and automated checks:

- Type check or compile
- Lint or format check
- Unit tests
- Integration or route tests
- Build
- OpenAPI/schema generation checks if present

When a local server can run, perform HTTP verification:

1. Start the server with the repo's script.
2. Exercise at least one happy path.
3. Exercise at least one validation or error path.
4. Exercise unauthenticated or unauthorized behavior when auth applies.
5. Confirm database state when the endpoint writes data.

Use `scripts/verify_api.py` for generic HTTP smoke checks. Use project-native tests for deeper assertions.

For detailed verification guidance, read `references/verification-checklist.md`.

## Final Response

When complete, report:

- What changed
- Key files touched
- API contract summary
- Static checks and tests run
- HTTP smoke checks run
- Any verification that could not run and why
- Remaining risk if any required fact could not be confirmed

Keep the final response concise and factual.
