# Schema Contract

Use this before writing tables, ORM models, migrations, or indexes.

## Table Contract Template

For each table, define:

```text
Table:
Purpose:
Source of truth:
Expected row count:
Write paths:
Read paths:
Retention/deletion:
Tenant/owner:

Columns:
- name:
  type:
  nullable:
  default:
  generated:
  validation:
  sensitive:
  notes:

Keys and constraints:
- primary key:
- foreign keys:
- unique constraints:
- check constraints:

Indexes:
- name:
  columns:
  order:
  predicate:
  supports query:

Migration:
- existing data impact:
- default/backfill:
- rollback:
```

## Constraints

Prefer database constraints for rules that must never be violated:

- `NOT NULL` for required facts
- `UNIQUE` for business uniqueness
- `FOREIGN KEY` for required relationships
- `CHECK` for ranges, non-negative values, status values, and date ordering
- Default values for safe creation paths

Use application validation too, but do not rely only on application validation for durable invariants.

## Foreign Keys

For each foreign key, decide:

- Required or optional
- Delete behavior: restrict, cascade, set null, soft-delete, archive
- Update behavior
- Whether child rows are owned by the parent
- Whether historical rows should survive parent changes

Avoid cascade delete for financial, audit, payment, compliance, or historical records unless the business rule is explicit.

## Unique Constraints

Make uniqueness match the business scope:

- Global: `email`
- Tenant-scoped: `(tenant_id, slug)`
- Time-scoped: `(resource_id, effective_date)`
- Relationship: `(left_id, right_id)` in join tables
- Idempotency: `(tenant_id, idempotency_key)` or `(external_system, external_id)`

Do not rely on pre-insert queries for uniqueness. They race under concurrency.

## Naming

Follow local conventions. If none exist, prefer:

- Tables: plural snake_case
- Columns: snake_case
- Primary key: `id`
- Foreign key: `<entity>_id`
- Timestamps: `created_at`, `updated_at`, `deleted_at`
- Indexes: `idx_<table>_<columns>`
- Unique indexes: `uniq_<table>_<columns>`
- Foreign keys: `fk_<table>_<column>`

## Index Justification

Every non-constraint index should name the query it supports.

Avoid indexes that are not tied to:

- A frequent filter
- A sort order
- A join path
- A uniqueness rule
- A selective partial condition

Each index has write and storage cost.

## Review Questions

Before implementing, check:

- Can invalid business states be inserted?
- Can duplicate records be created under concurrency?
- Can orphaned children exist?
- Can tenant data leak through missing scope?
- Can historical records change when current records change?
- Can a list query run unbounded?
- Can a migration be applied to existing production data?
- Can sensitive fields be safely logged, exported, or deleted?
