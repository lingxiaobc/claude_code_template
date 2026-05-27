# Testing Strategy

Use this when deciding which tests to add or run.

## Test Levels

Use the level that matches the risk:

- Unit tests: pure business logic, validators, small utilities
- Integration tests: routes, controllers, resolvers, database behavior
- E2E tests: critical flows through the full app
- Contract/schema tests: OpenAPI, GraphQL, generated clients
- Regression tests: bug reproduction
- Characterization tests: behavior lock before rewrite

## API Tests

Cover:

- Happy path
- Invalid body
- Invalid query/path params
- Unauthenticated request
- Forbidden request
- Not found
- Conflict
- Pagination/filter/sort
- Database side effects
- External dependency failure with mocks

## Optimization Tests

Add behavior regression tests first. Add benchmark or query-count checks only if the project has a pattern for them or the performance issue is central to the task.

## Rewrite Tests

Before rewriting, preserve old behavior with characterization tests. After rewriting, run the same tests against the new implementation.

## Fixtures

Use existing factories and fixtures. Avoid large test setup unless needed for the behavior under test.

## When Tests Cannot Be Added

If no test framework exists or setup is blocked, use HTTP smoke checks and report the limitation clearly.
