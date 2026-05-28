---
name: backend-engineering-workflow
description: "End-to-end backend engineering workflow for building backend services, creating, modifying, optimizing, debugging, testing, and documenting server endpoints, detecting backend risks, refactoring or rewriting backend code, and verifying server behavior. Use when the user asks to build a backend, create a server, implement backend features, add or adjust REST APIs, GraphQL resolvers, RPC handlers, controllers, routes, request validation, response schemas, authentication, authorization, pagination, filtering, sorting, OpenAPI/Swagger specs, backend integration tests, performance/error handling, database logic, or backend quality hardening. Do NOT use for frontend-only work, deployment-only tasks with no backend code change, database-only analysis with no service change, or high-level architecture discussion with no implementation."
---

# Backend Engineering Workflow

Use this skill for backend implementation, backend setup, API construction, optimization, detection, refactoring, and rewriting.

Follow seven phases:

1. Inspect
2. Diagnose
3. Plan
4. Contract
5. Implement
6. Verify
7. Report

Backend changes affect data, security, runtime behavior, and client contracts. Ground decisions in project files, schemas, tests, local conventions, official documentation, or explicit user confirmation.

## Resource Guide

Load these references only when needed:

- `references/project-recon.md`: Use during Inspect to identify framework, runtime, commands, routes, tests, database, auth, and docs.
- `references/task-diagnosis.md`: Use during Diagnose to classify the task as build, feature, API, bug, optimization, security, refactor, rewrite, or tests.
- `references/api-development.md`: Use for endpoint-focused REST, GraphQL, RPC, controller, route, request/response, OpenAPI, or HTTP verification work.
- `references/api-contract.md`: Use whenever the task changes API behavior, request/response schemas, auth, status codes, or side effects.
- `references/implementation-patterns.md`: Use during Implement for layering, validation, errors, logging, external calls, docs, and dependency rules.
- `references/optimization-workflow.md`: Use for performance, query, memory, latency, throughput, cache, or N+1 work.
- `references/rewrite-workflow.md`: Use for refactors and rewrites that must preserve behavior.
- `references/security-review.md`: Use whenever auth, user data, tenant boundaries, files, webhooks, secrets, payment, or external services are involved.
- `references/database-and-migrations.md`: Use whenever models, schema, migrations, indexes, transactions, queries, or data shape are involved.
- `references/testing-strategy.md`: Use when adding or choosing tests.
- `references/verification-checklist.md`: Use during Verify and before final response.

Use these scripts as black-box helpers. Run each with `--help` before use:

- `scripts/inspect_backend.py`: Project reconnaissance report in JSON.
- `scripts/verify_api.py`: Generic HTTP smoke checks for local or remote endpoints.
- `scripts/scan_backend_risks.py`: Static scan for common backend risk patterns.
- `scripts/benchmark_endpoint.py`: Basic endpoint latency benchmark for optimization work.

Use these reviewer prompts when subagents are available and the change is high-risk:

- `agents/api-contract-reviewer.md`
- `agents/security-reviewer.md`
- `agents/test-coverage-reviewer.md`

## Phase 1: Inspect

Inspect before editing. Do not guess the framework, ORM, auth system, route layout, validation library, test command, or deployment shape.

Find:

- Runtime, language, framework, and package manager
- App entrypoint, route/controller/resolver layout, and service layers
- Database/ORM schema, migrations, repositories, and generated types
- Auth middleware, guards, policies, roles, tenant scoping, and session/current-user handling
- Validation and serialization patterns
- Error response shape and logging conventions
- Existing tests and fixtures
- Build, typecheck, lint, test, and dev server commands
- API documentation or schema generation

Run `scripts/inspect_backend.py` for a first pass, then read the relevant files it identifies. For detailed guidance, read `references/project-recon.md`.

## Phase 2: Diagnose

Classify the task before planning. Determine whether it is:

- Backend setup or new service construction
- Feature implementation
- API addition or modification
- Bug investigation and fix
- Performance optimization
- Security hardening
- Refactor
- Rewrite
- Test coverage improvement
- Documentation or schema update

The task type changes the workflow. For example, bug fixes need reproduction, optimizations need baseline measurements, and rewrites need behavior-locking tests.

For endpoint-focused API work, load `references/api-development.md` after diagnosis and use it with `references/api-contract.md`.

For detailed guidance, read `references/task-diagnosis.md`.

## Phase 3: Plan

Choose the smallest implementation path that satisfies the request.

Plan:

- Files likely to change
- Behavior that must remain unchanged
- Contracts or schemas that must be updated
- Tests needed
- Verification commands
- Risks and facts that still need confirmation

Prefer existing patterns. Avoid broad refactors, new dependencies, framework swaps, or unrelated style churn.

## Phase 4: Contract

Use a contract phase whenever the work touches an API, database behavior, permission rule, external side effect, background job, or public module behavior.

Define:

- Inputs
- Outputs
- Validation
- Errors
- Auth and permission rules
- Database reads and writes
- Side effects
- Backward compatibility
- Tests and verification

For API work, read `references/api-contract.md`.

## Phase 5: Implement

Implement according to the contract and local codebase style.

Rules:

- Reuse local framework, routing, validation, error, logging, service, repository, and test patterns.
- Keep business logic in the layer where the project already puts it.
- Validate all user-controlled inputs.
- Use existing auth and permission mechanisms.
- Preserve public behavior unless the user requested a breaking change.
- Use transactions for multi-step writes that must remain consistent.
- Avoid raw SQL string interpolation.
- Avoid leaking secrets, stack traces, tokens, or private data.
- Add or update focused tests when a test path exists.

Load the relevant reference files for the task type.

## Phase 6: Verify

Do not finish after writing code. Verify with the strongest checks available.

Run applicable commands:

- Typecheck or compile
- Lint or format check
- Unit tests
- Integration or route tests
- Build
- API schema generation
- HTTP smoke checks
- Risk scan
- Benchmark when optimizing

Use `scripts/verify_api.py` for generic HTTP checks and `scripts/scan_backend_risks.py` for risk scanning. Use `scripts/benchmark_endpoint.py` only when measuring endpoint performance.

For detailed guidance, read `references/verification-checklist.md`.

## Phase 7: Report

Final response should include:

- What changed
- Key files touched
- Contract or behavior summary
- Tests and checks run
- HTTP or benchmark verification run, if applicable
- Any checks that could not run and why
- Remaining risks or facts that could not be confirmed

Keep the response concise and factual.
