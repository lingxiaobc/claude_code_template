# Verification Checklist

Use this before final response.

## Schema Correctness

Check:

- Tables have primary keys
- Required facts are `NOT NULL`
- Business uniqueness has unique constraints
- Relationships have foreign keys or a documented alternative
- Optional relationships have clear null semantics
- Delete behavior is explicit
- Money and precise quantities do not use float
- Timestamps use the project convention and timezone strategy
- Tenant-scoped tables include tenant/organization scope
- Audit and soft-delete conventions are followed

## Migration Safety

Check:

- Migration follows local framework conventions
- Existing rows are handled
- Backfill is safe and idempotent when needed
- Rollback or forward-fix path is understood
- Generated ORM/types were updated when required
- Large-table operations avoid unnecessary locks when possible
- Destructive operations are intentional and documented

## Query and Index Quality

Check:

- Indexes map to real access patterns
- No unbounded list query was introduced
- Pagination has stable ordering
- High-traffic joins have supporting indexes
- Query plans were reviewed for performance-sensitive changes
- Added indexes do not duplicate existing indexes unnecessarily

## Security

Check:

- Tenant and ownership filters exist where required
- Sensitive data is not logged or exposed
- Secrets are not stored in plaintext
- User-controlled sort/filter identifiers are allowlisted
- SQL values are parameterized
- Deletion/retention behavior matches requirements

## Concurrency

Check:

- Multi-row writes use transactions
- Duplicate prevention uses database constraints
- Idempotency exists for retried external operations
- Status transitions validate current state
- Locks are short-lived and not held during slow external calls

## Commands To Run

Run available checks:

- Migration generation/diff
- Migration apply on local/test database
- Migration rollback when supported
- ORM/client generation
- Unit/integration tests
- Repository/query tests
- Static risk scan:

```bash
python scripts/scan_schema_risks.py --help
python scripts/scan_schema_risks.py .
```

## Final Response

Report:

- What changed
- Key schema decisions
- Migration/backfill behavior
- Constraints and indexes added
- Tests/checks run
- Checks not run and why
- Remaining assumptions or risks
