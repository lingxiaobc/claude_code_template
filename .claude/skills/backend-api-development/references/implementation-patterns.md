# Implementation Patterns

Use this file during implementation.

## Follow Existing Layers

Match the project's architecture:

- Route/controller/resolver: request parsing, auth hooks, response mapping
- Validator/DTO/schema/serializer: input and output shape
- Service/use case: business logic
- Repository/data access: database queries
- Model/entity/schema: persistence shape
- Tests: unit, integration, e2e, fixtures

If the project is intentionally simple and keeps logic in route handlers, follow that pattern without adding ceremony.

## Validation

Use the validation approach already present:

- Zod, Joi, Yup, Valibot
- class-validator DTOs
- Pydantic models
- Django serializers/forms
- Rails validations
- Laravel FormRequest
- Go validator/binding tags
- Java Bean Validation

Validate all user-controlled inputs:

- Path params
- Query params
- Request body
- Headers used for behavior
- File metadata
- Webhook payloads

Keep validation errors in the project's existing response format.

## Error Handling

Reuse existing helpers and exception types. Preserve the established shape for:

- Validation errors
- Unauthorized errors
- Forbidden errors
- Not found errors
- Conflict errors
- Internal errors

Do not return raw exceptions or stack traces.

When an error is actionable for API clients, include stable error codes if the project uses them.

## Documentation and Schemas

If the project maintains API documentation, update it with the implementation:

- OpenAPI/Swagger decorators or schema files
- GraphQL schema and generated types
- RPC schema definitions
- Typed API clients
- Postman/Bruno collections if maintained

Do not create a parallel documentation system if the project already has one.

## Optimization and Adjustment Work

When optimizing an existing API:

1. Identify the bottleneck from code, logs, query plans, tests, or measurable symptoms.
2. Preserve the public contract unless the user requests a breaking change.
3. Prefer targeted fixes: indexes, query shape, pagination, batching, caching, serialization, or N+1 reduction.
4. Add regression tests where behavior could change.
5. Measure before and after when the environment supports it.

Avoid speculative rewrites.

## Dependencies

Do not add dependencies unless:

- The project already uses the dependency,
- The user explicitly approves it, or
- The implementation is impractical without it and you explain why.

Prefer standard library and existing project utilities.

## Backward Compatibility

Before changing an existing endpoint:

- Check existing tests and docs.
- Keep existing response fields unless removing them is requested.
- Add optional fields instead of changing field meaning.
- Consider versioning if behavior changes substantially.
- Preserve status-code semantics where clients may depend on them.

## Tests

Add or update focused tests when there is a test path.

Useful tests:

- Happy path
- Validation failure
- Unauthorized
- Forbidden
- Not found
- Conflict
- Pagination/filter/sort behavior
- Database write side effects
- External service failure with mock

Prefer integration tests for route behavior and unit tests for complex business logic.
