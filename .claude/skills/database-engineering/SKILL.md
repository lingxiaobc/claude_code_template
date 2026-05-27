---
name: database-engineering
description: "End-to-end database engineering workflow for designing relational data models, writing schemas and migrations, reviewing constraints, creating indexes, optimizing queries, and hardening persistence behavior. Use when the user asks to design a database, create or change tables, choose fields/types/keys, model entity relationships, write SQL/ORM migrations, review database schema quality, improve slow queries, add indexes, plan transactions, handle multi-tenant data, or evaluate data integrity/security risks. Do NOT use for frontend-only work, one-off spreadsheet analysis, or high-level product brainstorming with no persisted data model."
---

# Database Engineering

Use this skill for database design, schema implementation, migration planning, query optimization, and data integrity review.

Follow seven phases:

1. Inspect
2. Model
3. Contract
4. Implement
5. Optimize
6. Verify
7. Report

Database changes define durable business facts. Ground decisions in product requirements, existing schema, migrations, ORM models, query code, data volume, access patterns, and explicit user confirmation. Do not invent tables, fields, relationships, enum values, retention rules, or performance requirements.

## Resource Guide

Load these references only when needed:

- `references/project-recon.md`: Use during Inspect to identify database engine, ORM, migration workflow, schemas, seeds, tests, and runtime commands.
- `references/data-modeling.md`: Use when designing entities, fields, relationships, normalization, denormalization, snapshots, enums, and JSON columns.
- `references/schema-contract.md`: Use before writing or changing tables, constraints, foreign keys, indexes, or ORM models.
- `references/migrations-and-evolution.md`: Use whenever schema changes require migrations, backfills, compatibility, rollbacks, or large-table changes.
- `references/indexing-and-query-plans.md`: Use for query performance, indexes, sorting, filtering, pagination, joins, and execution plans.
- `references/transactions-and-concurrency.md`: Use when writes span multiple rows/tables, counters, inventory, balances, status transitions, idempotency, or locks.
- `references/security-and-compliance.md`: Use when data includes users, tenants, permissions, PII, secrets, payments, audit logs, retention, or deletion.
- `references/optimization-workflow.md`: Use for slow queries, high load, database bottlenecks, storage growth, or performance regressions.
- `references/verification-checklist.md`: Use before final response.

Use these scripts as black-box helpers. Run each with `--help` before use:

- `scripts/inspect_database_project.py`: Project reconnaissance report in JSON.
- `scripts/scan_schema_risks.py`: Static scan for common schema, migration, and query risk patterns.

## Phase 1: Inspect

Inspect before designing or editing. Do not guess the database engine, ORM, migration tool, naming style, ID strategy, tenant model, cascade behavior, or query patterns.

Find:

- Database engine and version when available
- ORM or query builder
- Schema/model definitions
- Migration files and migration command
- Seed, fixture, factory, and test data patterns
- Existing naming conventions for tables, columns, indexes, constraints, and timestamps
- Current primary key, foreign key, enum, soft-delete, audit, and tenant conventions
- Read/write access paths in routes, services, repositories, jobs, and reports
- Existing indexes and slow-query evidence when available
- Backup, retention, data deletion, or compliance constraints if documented

Run `scripts/inspect_database_project.py` for a first pass, then read the relevant files it identifies. For detailed guidance, read `references/project-recon.md`.

## Phase 2: Model

Model the data before writing DDL or ORM code.

Define:

- Business entities and aggregate boundaries
- Attributes and which facts are canonical
- Entity relationships: one-to-one, one-to-many, many-to-many, optional, required
- Identity strategy: surrogate keys, natural keys, public IDs, tenant-scoped IDs
- Required fields, nullable fields, defaults, and generated fields
- Field types, precision, length, timezone, collation, and units
- Unique constraints and business invariants
- Lifecycle states and allowed transitions
- Historical snapshots needed for correctness
- Delete/archive behavior and retention requirements
- Expected read and write access patterns

For new designs, read `references/data-modeling.md`.

## Phase 3: Contract

Create a schema contract before implementation.

For each table or collection, specify:

- Purpose and source of truth
- Columns with type, nullability, default, and validation rules
- Primary key and public identifier
- Foreign keys and relationship cardinality
- Unique constraints and check constraints
- Indexes justified by access patterns
- Ownership, tenant, and authorization fields
- Audit fields and soft-delete fields
- Migration/backfill requirements
- Example queries the schema must support

For detailed contract guidance, read `references/schema-contract.md`.

## Phase 4: Implement

Implement using the project's established database layer.

Rules:

- Use existing migration, ORM, naming, timestamp, and test patterns.
- Prefer database constraints for invariants that must always hold.
- Use foreign keys unless the project deliberately avoids them and has a documented alternative.
- Use precise types for money, counts, timestamps, and identifiers.
- Avoid raw SQL string interpolation.
- Preserve existing data and application compatibility unless the user requested a breaking migration.
- Add focused tests, fixtures, or seed changes when the project has test infrastructure.
- Keep migrations reversible when the local migration system supports it.

For migration details, read `references/migrations-and-evolution.md`.

## Phase 5: Optimize

Optimize from evidence, not intuition.

Use:

- Query plan
- Slow query log
- Reproduction query
- Endpoint benchmark
- Database metrics
- User report tied to a concrete access path

Prefer targeted fixes: query shape, correct indexes, pagination, batched loading, reduced overfetching, materialized summaries, partitioning, or caching with clear invalidation. For detailed guidance, read `references/optimization-workflow.md` and `references/indexing-and-query-plans.md`.

## Phase 6: Verify

Do not finish after writing schema or query code. Verify with the strongest checks available.

Run applicable checks:

- Migration generation or dry-run
- Migration apply against a local/test database
- Migration rollback when supported
- ORM type generation
- Unit, integration, repository, or API tests
- Static schema risk scan
- Query plan review for changed high-traffic queries
- Data backfill validation
- Tenant/authorization tests for scoped data

Use `scripts/scan_schema_risks.py` for a first-pass risk scan. For detailed QA guidance, read `references/verification-checklist.md`.

## Phase 7: Report

Final response should include:

- What data model or schema changed
- Key tables, columns, relationships, constraints, and indexes
- Migration/backfill behavior
- Query or performance implications
- Tests and checks run
- Any verification that could not run and why
- Remaining risks or assumptions

Keep the response concise and factual.
