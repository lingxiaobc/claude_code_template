# Transactions and Concurrency

Use this when correctness depends on multiple writes, counters, balances, inventory, idempotency, or state transitions.

## Transaction Boundaries

Use transactions when operations must succeed or fail together:

- Parent row plus child rows
- Payment record plus order status
- Balance movement plus ledger entry
- Inventory reservation plus order item
- Status transition plus audit event
- Outbox event plus state change

Use the project's existing transaction helper or unit-of-work pattern.

## Isolation

Understand what can go wrong:

- Dirty reads
- Non-repeatable reads
- Phantom reads
- Lost updates
- Write skew
- Duplicate insert race

Use database constraints first for uniqueness and integrity. Use locks or stronger isolation only where needed.

## Idempotency

For external retries, webhooks, payments, imports, or background jobs:

- Accept an idempotency key or external event ID
- Store it with a unique constraint
- Make retries return the same logical result
- Keep side effects behind the idempotency guard

Do not rely on "check then insert" without a unique constraint.

## State Transitions

For lifecycle states:

- Validate current state in the update condition
- Record transition timestamp
- Record actor when relevant
- Add audit/event row when history matters

Example pattern:

```sql
UPDATE orders
SET status = 'paid', paid_at = now()
WHERE id = $1 AND status = 'pending';
```

Then check affected row count.

## Locks

Use locks deliberately:

- Row lock for single-record critical sections
- Advisory lock for cross-row or external resource coordination
- Optimistic lock with `version` for user-editable records
- Unique constraint for duplicate prevention

Keep transactions short. Do not hold locks during slow external calls.

## Counters and Derived Values

For counters:

- Prefer deriving from source rows unless performance requires storage
- If stored, define update path and reconciliation query
- Use atomic increments when supported
- Recalculate or validate periodically for critical counters

## External Side Effects

Do not call external services inside a transaction unless unavoidable.

Prefer:

- Write durable state
- Commit transaction
- Use outbox/job/event to perform external side effect
- Mark outcome after side effect completes

This prevents holding database locks while waiting on networks.
