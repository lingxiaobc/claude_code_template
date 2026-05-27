# Task Diagnosis

Use this during the Diagnose phase.

## Classify The Task

Determine the main task type:

- New backend service or setup
- Feature implementation
- API creation or modification
- Bug fix
- Performance optimization
- Security hardening
- Refactor
- Rewrite
- Test coverage
- Documentation/schema update

Many tasks combine types. Pick the highest-risk type as the primary workflow.

## New Backend Or Service Setup

Confirm:

- Runtime and framework requested
- API style: REST, GraphQL, RPC, WebSocket, background worker
- Database, cache, queue, and external services
- Auth requirements
- Environment/config strategy
- Test strategy
- Local run command

Start with a minimal runnable service and one verified endpoint before adding breadth.

## Feature Or API Work

Use the contract workflow. Confirm request shape, response shape, auth, data writes, error behavior, and tests before coding.

## Bug Fix

Before fixing:

1. Reproduce the bug or identify the failing test.
2. Locate the smallest failing behavior.
3. Add or update a regression test when practical.
4. Fix the cause, not just the symptom.
5. Run the regression test and relevant suite.

If reproduction is impossible, state the observed evidence and remaining uncertainty.

## Performance Optimization

Before optimizing:

1. Establish a baseline or identify existing measurement.
2. Locate likely bottleneck with evidence.
3. Preserve the public contract.
4. Make a targeted change.
5. Measure after.

Avoid speculative rewrites.

## Security Hardening

Treat auth, tenant boundaries, secrets, file handling, webhooks, and external requests as high risk. Read `security-review.md`.

## Refactor

A refactor should preserve externally visible behavior. Identify existing tests. Add characterization tests if behavior is under-tested.

## Rewrite

A rewrite is riskier than a refactor. Read `rewrite-workflow.md`. Lock existing behavior first. Do not combine rewrite with product behavior changes unless the user explicitly asks.

## Test Coverage

Identify what behavior matters, then add tests at the right level. Prefer integration tests for routes and unit tests for complex business logic.

## Ask The User When

Ask before implementation when the answer cannot be found locally and affects:

- Permission rules
- Data model or business rules
- Billing, money, inventory, or irreversible side effects
- Public API compatibility
- Migration/backfill strategy
- External service behavior
