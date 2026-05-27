# Project Recon

Use this during Inspect before designing or changing database code.

## First Pass

Identify the database stack:

- Engine: PostgreSQL, MySQL/MariaDB, SQLite, SQL Server, Oracle, MongoDB, DynamoDB, Redis, or other
- Access layer: raw SQL, Prisma, Drizzle, TypeORM, Sequelize, Knex, SQLAlchemy, Django ORM, Rails ActiveRecord, Entity Framework, Ecto, Hibernate, JPA, GORM, Diesel, Liquibase, Flyway, Alembic, dbt
- Migration location and naming convention
- Schema/model definitions
- Seed data, fixtures, factories, and test database setup
- Generated clients or type generation commands
- Local database startup and reset commands
- Existing docs: ERD, ADRs, runbooks, API contracts, schema comments

Run:

```bash
python scripts/inspect_database_project.py --help
python scripts/inspect_database_project.py .
```

Then read the files it reports.

## Files To Search

Common locations:

- `prisma/schema.prisma`
- `drizzle.config.*`, `src/db/schema.*`
- `db/schema.rb`, `db/migrate/*`
- `migrations/*`, `alembic/versions/*`
- `models.py`, `entities/*`, `models/*`, `repositories/*`
- `knexfile.*`, `sequelize-cli`, `typeorm.config.*`
- `liquibase/*`, `flyway/*`, `db/changelog/*`
- `*.sql`, `schema.sql`, `init.sql`

## Facts To Capture

Capture these before planning:

- Primary key strategy
- Timestamp convention
- Soft-delete convention
- Tenant/organization scoping
- Audit fields and audit tables
- Foreign key and cascade conventions
- Enum representation
- Money/decimal representation
- JSON column usage
- Existing index naming and composite index style
- Pagination and sorting conventions
- Transaction helper APIs
- Test command and migration command

## Questions Worth Asking

Ask the user only when the answer cannot be discovered and the wrong assumption would cause rework:

- Expected database engine and deployment environment
- Approximate row counts and growth rate
- High-traffic read/write paths
- Retention, deletion, compliance, or audit requirements
- Whether historical records must preserve values after related entities change
- Whether data is single-tenant or multi-tenant
- Whether downtime is acceptable for migration

## Do Not Guess

Do not invent:

- Table or column names
- Relationship cardinality
- Cascade behavior
- Tenant scope
- Whether null means unknown, not applicable, not yet set, or deleted
- Whether IDs can be exposed publicly
- Whether existing data can be rewritten or dropped
