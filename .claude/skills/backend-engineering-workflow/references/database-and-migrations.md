# Database and Migrations

Use this when backend work depends on data models, queries, schema changes, migrations, indexes, transactions, or persistence behavior.

## Fact Sources

Confirm data shape from:

- ORM schema
- Model/entity class
- Migration
- SQL schema
- Existing repository/query code
- Generated types

Do not invent fields, tables, relations, enum values, indexes, or cascade behavior.

## Schema Changes

When adding persisted data:

- Update the project schema/model.
- Add migration if the project uses migrations.
- Update generated types or clients if required.
- Add tests and fixtures.
- Consider defaults and backfills for existing rows.

Do not create migrations without understanding the local migration workflow.

## Transactions

Use transactions for writes that must remain consistent:

- Parent and child rows
- Status update plus audit row
- Balance/count updates
- Multi-table delete/archive
- Outbox pattern where project supports it

Use existing transaction helpers.

## List Queries

Avoid unbounded reads.

For list endpoints:

- Match existing pagination style.
- Enforce maximum page size.
- Use stable sort order.
- Add metadata if the project does.
- Consider indexes for new filters or sort keys.

## Delete Behavior

Before deleting:

- Check soft-delete conventions.
- Check cascade behavior.
- Check tenant/ownership filters.
- Check audit requirements.
- Check whether related resources block deletion.

## Test Data

Use existing factories, fixtures, or seed helpers. Keep new test data minimal and explicit.
