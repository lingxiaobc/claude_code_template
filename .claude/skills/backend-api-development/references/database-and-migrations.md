# Database and Migrations

Use this file when endpoint behavior depends on data models, schema changes, migrations, indexes, or database writes.

## Schema Is the Fact Source

Confirm data shape from:

- ORM schema
- Model/entity class
- Migration
- SQL schema
- Existing query/repository code
- Generated types
- API docs only if they are known to be current

Do not invent fields, relations, enum values, indexes, or table names.

## Model Changes

When the API needs new persisted data:

- Update the model/schema in the project's established location.
- Add a migration if the project uses migrations.
- Update generated clients or types if the project requires it.
- Update tests and fixtures.
- Consider backfill or default behavior for existing rows.

Do not create schema changes without understanding migration workflow.

## Transactions

Use transactions for multi-step writes that must remain consistent:

- Create parent and child rows
- Update balance/count/status and create audit row
- Write database row and enqueue related job when the project supports transactional outbox
- Delete or archive multiple related records

If the project has transaction helpers, use them.

## Pagination and Query Limits

Avoid unbounded reads.

For list endpoints:

- Match existing pagination style.
- Enforce maximum page size.
- Use stable sort order.
- Include pagination metadata if the project uses it.
- Consider indexes for new filters or sort keys.

## Filters and Sorting

Use allowlisted fields.

Avoid passing raw user-controlled strings into:

- SQL column names
- ORM order objects
- Include/expand relation names
- Raw where clauses

## Deletion

Before implementing delete:

- Check whether the project uses soft delete.
- Check cascade behavior.
- Check ownership and tenant filters.
- Check audit requirements.
- Check whether related resources block deletion.

## Performance

Watch for:

- N+1 queries
- Overfetching large relations
- Missing indexes for new filters
- Large JSON serialization
- Unbounded joins
- Per-row external service calls

Prefer targeted query changes over broad rewrites.

## Test Data

Use existing fixtures, factories, or seed helpers.

If creating new test data:

- Keep it minimal.
- Include edge cases relevant to validation and permissions.
- Clean up according to project test conventions.
