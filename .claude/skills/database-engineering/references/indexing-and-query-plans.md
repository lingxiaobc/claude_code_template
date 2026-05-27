# Indexing and Query Plans

Use this for query performance, indexes, joins, sorting, filtering, and pagination.

## Start From Access Patterns

Do not add indexes by guessing. Capture:

- Query text or ORM query
- Filters
- Joins
- Sort order
- Pagination style
- Expected row count
- Selectivity of each filter
- Frequency and latency requirement

## Common Index Patterns

Use indexes for:

- Foreign keys used in joins
- High-cardinality equality filters
- Composite filters used together
- Sort plus filter paths
- Unique business rules
- Partial queries on active rows, such as `deleted_at IS NULL`

Composite index order matters. Put equality filters first, then range/sort columns when it matches the query.

## Pagination

Avoid unbounded reads.

Prefer:

- Stable sort order
- Keyset pagination for large or frequently changing lists
- Maximum page size
- Index that matches filter and sort

Offset pagination can become expensive for deep pages and can skip/duplicate rows under concurrent writes.

## Query Shape

Check for:

- `SELECT *` when only a few fields are needed
- N+1 queries
- Overfetching large relations
- Filtering in application code after fetching many rows
- Sorting without a supporting index
- Functions on indexed columns that prevent index use
- Leading wildcard searches
- Implicit casts
- Nullable filters with poor selectivity

## Execution Plans

Use the database's explain tool:

- PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS)`
- MySQL: `EXPLAIN ANALYZE` or `EXPLAIN FORMAT=JSON`
- SQLite: `EXPLAIN QUERY PLAN`
- SQL Server: actual execution plan

Review:

- Sequential scans on large tables
- Index scan vs index only scan
- Join order and join algorithm
- Estimated rows vs actual rows
- Sort nodes
- Temporary files or disk spills
- Buffer reads
- Lock waits

Do not overreact to a sequential scan on a small table.

## Index Tradeoffs

Each index costs:

- Storage
- Insert/update/delete overhead
- Vacuum/maintenance work
- Migration time
- Planner complexity

Remove or avoid redundant indexes. For example, an index on `(tenant_id, created_at)` may make a separate `(tenant_id)` index unnecessary depending on queries.

## When Not To Add An Index

Avoid indexes when:

- The table is tiny and will remain tiny
- The filter is low-cardinality and not paired with selective columns
- The query is rare and latency is acceptable
- The problem is N+1 or overfetching, not access path
- A better data model or summary table is needed

## Reporting Optimization

When optimizing, report:

- Original query or access path
- Evidence of slowness
- Change made
- Indexes added or removed
- Before/after timing or plan difference if measured
- Tradeoffs and residual risks
