# Optimization Workflow

Use this for backend performance, latency, throughput, query, memory, cache, or N+1 work.

## Baseline First

Do not optimize from intuition alone. Establish evidence:

- Slow test or user report
- Logs or traces
- Benchmark result
- Query plan
- Reproduction case
- Existing metric

Use `scripts/benchmark_endpoint.py` for simple endpoint latency baselines when a local HTTP endpoint is available.

## Common Bottlenecks

Check:

- N+1 queries
- Missing pagination
- Missing indexes
- Overfetching large relations
- Repeated serialization work
- Per-row external service calls
- Unbounded loops
- Expensive synchronous work in request path
- Cache misses or invalidation bugs
- Large payloads
- Connection pool issues

## Optimization Rules

- Preserve public contract unless the user asked for a breaking change.
- Make targeted changes.
- Prefer query shape, indexes, batching, pagination, caching, and serialization improvements before broad rewrites.
- Add regression tests for behavior.
- Measure after the change when possible.
- Report before/after data if measured.

## Database Query Optimization

Confirm schema and indexes. Consider:

- Select only needed fields
- Add stable pagination
- Use joins/includes carefully
- Batch related fetches
- Add index migrations when needed and appropriate
- Avoid raw SQL unless project conventions support it

## Cache Changes

Before adding cache:

- Define key shape
- Define invalidation behavior
- Define TTL
- Define consistency tolerance
- Define test strategy

Do not add cache when the correctness model is unclear.
