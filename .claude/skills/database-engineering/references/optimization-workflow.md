# Optimization Workflow

Use this for slow queries, high database load, storage growth, or performance regressions.

## Baseline First

Do not optimize from intuition alone.

Collect at least one:

- Slow query log
- Query text and parameters
- `EXPLAIN` or execution plan
- Endpoint benchmark
- Database metrics
- User report with reproducible filters
- Row counts and data distribution

## Diagnose

Classify the bottleneck:

- Missing or mismatched index
- N+1 queries
- Overfetching columns or relations
- Expensive sort
- Bad pagination
- Join explosion
- Lock contention
- Connection pool saturation
- Large transaction
- Hot row or counter
- Cache miss or invalidation issue
- Storage bloat or maintenance issue

The fix depends on the bottleneck.

## Preferred Fix Order

Prefer low-risk targeted changes:

1. Select fewer fields
2. Add pagination or limit
3. Batch related reads
4. Remove N+1 query pattern
5. Add or adjust index
6. Rewrite query shape
7. Add summary/materialized table
8. Add cache with explicit invalidation
9. Partition/archive data
10. Consider broader model change

## Caching

Before adding cache, define:

- Cache key
- TTL
- Invalidation trigger
- Consistency tolerance
- Stampede prevention
- Authorization/tenant scope in key
- Test strategy

Do not add cache when stale data would violate correctness.

## Write Path Performance

Check:

- Too many indexes
- Large transactions
- Cascading writes
- Synchronous external calls
- Hot counters
- Full-row updates of large records
- Locking reads

Optimizing reads by adding indexes can slow writes. Report the tradeoff.

## Measure After

After a change, re-run the baseline when possible.

Report:

- Before timing or plan
- After timing or plan
- Indexes changed
- Query shape changed
- Residual risks

If measurement is impossible, say so and explain the expected effect from the plan or query shape.
