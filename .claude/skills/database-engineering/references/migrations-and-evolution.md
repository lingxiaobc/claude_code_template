# Migrations and Evolution

Use this whenever schema changes must be applied to an existing database.

## Migration Principles

Migrations change durable data. Treat them as production code.

Before writing a migration:

- Identify the local migration tool and naming convention
- Read recent migrations for style
- Determine whether migrations are reversible
- Check whether generated ORM clients or types must be updated
- Decide how existing rows will be handled
- Estimate table size and lock risk when possible

## Safe Change Pattern

For application deployments with existing data, prefer expand-contract:

1. Add new nullable column/table/index without breaking old code
2. Deploy code that writes both old and new shape if needed
3. Backfill existing data
4. Deploy code that reads the new shape
5. Add stricter constraints after data is valid
6. Remove old shape in a later migration

Avoid combining incompatible schema changes and application code changes in one risky step.

## Adding Columns

Consider:

- Nullable or non-null
- Default value
- Existing row backfill
- Locking behavior for the database engine
- Whether a generated column is better
- Whether a check constraint should be added after backfill

For large tables, avoid table rewrites when the engine would lock or rewrite every row.

## Changing Column Types

Before changing a type:

- Confirm all existing values can convert
- Write validation queries
- Consider adding a new column and backfilling instead
- Check indexes and constraints using the column
- Check application serialization/deserialization

Never assume a type change is safe because sample data converts.

## Renaming

Renaming columns or tables can break deployed old code.

Prefer compatibility steps when zero downtime matters:

- Add new name
- Dual-write or sync
- Backfill
- Switch readers
- Remove old name later

## Backfills

For backfills:

- Make the operation idempotent
- Process in batches for large tables
- Log progress
- Avoid long transactions unless the table is small
- Validate before and after
- Keep retry behavior safe

## Index Migrations

For production databases:

- Use concurrent/online index creation if supported and required
- Avoid blocking writes on high-traffic tables
- Add partial indexes when they match a selective predicate
- Drop unused indexes only after confirming they are unused

PostgreSQL example preference: `CREATE INDEX CONCURRENTLY` for large live tables when the migration framework supports non-transactional migrations.

## Rollback

Define what rollback means:

- Schema rollback only
- Code rollback compatibility
- Data rollback
- Irreversible but safe forward-fix

Dropping columns, truncating data, and destructive conversions may not be safely reversible. State this explicitly.

## Verification Queries

Write validation queries for:

- Nulls before adding `NOT NULL`
- Duplicate values before adding `UNIQUE`
- Orphans before adding `FOREIGN KEY`
- Invalid enum/status values before adding checks
- Row counts before and after backfill
- Sample rows after data transformation
