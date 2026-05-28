# Implementation Patterns

Use this during implementation.

## Match Local Architecture

Follow the existing shape:

- Route/controller/resolver for transport concerns
- Validator/DTO/schema/serializer for input and output shape
- Service/use-case layer for business logic
- Repository/data access layer for queries
- Model/entity/schema for persistence
- Test fixtures/factories for setup

Do not add layers where the project is intentionally simple.

## Validation

Use the project's validation tool:

- Zod, Joi, Yup, Valibot
- class-validator DTOs
- Pydantic
- Django serializers
- Rails model/request validations
- Laravel FormRequest
- Go binding/validator
- Java Bean Validation

Validate path params, query params, body, behavior-driving headers, file metadata, and webhook payloads.

## Errors

Reuse existing error helpers and exception classes.

Preserve:

- Error shape
- Stable error codes
- Status-code conventions
- Logging behavior

Do not return raw exceptions, stack traces, SQL errors, or provider errors to clients.

## Logging

Use the existing logger. Log enough to debug, but do not log secrets, tokens, passwords, full authorization headers, or sensitive request bodies.

Include correlation/request IDs when the project supports them.

## External Services

Use configured clients. Handle:

- Timeouts
- Retries where safe
- Provider errors
- Idempotency
- Test mocks

Do not put long external calls inside transactions unless the project explicitly does so.

## Dependencies

Avoid new dependencies unless:

- The project already uses them,
- The user approves them, or
- The implementation is impractical without them and the reason is explained.

## Documentation

Update existing documentation systems when present:

- OpenAPI/Swagger
- GraphQL schema
- RPC schema
- Typed clients
- API collections

Do not create a parallel documentation system.

## API Optimization And Adjustment

When optimizing or adjusting an existing API:

1. Identify the bottleneck from code, logs, query plans, tests, or measurable symptoms.
2. Preserve the public contract unless the user requests a breaking change.
3. Prefer targeted fixes: indexes, query shape, pagination, batching, caching, serialization, or N+1 reduction.
4. Add regression tests where behavior could change.
5. Measure before and after when the environment supports it.

Avoid speculative rewrites.

## Backward Compatibility

Before changing an existing endpoint or public service behavior:

- Check existing tests and docs.
- Keep existing response fields unless removing them is requested.
- Add optional fields instead of changing field meaning.
- Preserve status-code semantics where clients may depend on them.
- Consider versioning if behavior changes substantially.

## Tests

Add or update focused tests when there is a test path.

Useful tests:

- Happy path
- Validation failure
- Unauthorized
- Forbidden
- Not found
- Conflict
- Pagination, filtering, and sorting behavior
- Database write side effects
- External service failure with mocks

Prefer integration tests for route behavior and unit tests for complex business logic.
