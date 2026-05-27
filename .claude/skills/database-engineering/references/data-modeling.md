# Data Modeling

Use this for new database designs or substantial changes to existing models.

## Model From Business Facts

Start with facts the system must remember:

- Who or what exists?
- What events happen?
- Which facts change over time?
- Which facts must be historically preserved?
- Which facts are derived and can be recalculated?
- Which facts must be unique?
- Which facts define permissions, ownership, or tenancy?

Avoid starting from screens alone. Screens change; durable business facts are the schema.

## Entities

For each entity define:

- Name and purpose
- Source of truth
- Required attributes
- Optional attributes
- Lifecycle states
- Owner or tenant
- Creation and update actor
- Retention and deletion behavior

Prefer singular business concepts, then map to the project's table naming convention.

## Relationships

Classify every relationship:

- One-to-one
- One-to-many
- Many-to-many through a join table
- Optional or required
- Immutable or mutable
- Owned child or independently managed entity

For many-to-many relationships, use a join table with:

- Foreign keys to both sides
- Unique constraint on the pair
- Additional attributes when the relationship has meaning, such as role, status, rank, or timestamps

## Identity

Use a surrogate primary key for most application tables unless the project has a different convention.

Consider:

- Internal primary key: `id`
- Public identifier: `public_id`, `slug`, or `uuid`
- Business unique key: `email`, `order_number`, `external_id`
- Tenant-scoped uniqueness: `(tenant_id, slug)` rather than global `slug`

Do not use mutable business data as a primary key.

## Field Types

Choose types that match semantics:

- Money: fixed precision decimal or integer minor units, never float
- Counts and quantities: integer or decimal depending on fractional needs
- Timestamps: timezone-aware when the engine supports it
- Dates without time: date type, not timestamp
- Durations: integer seconds/milliseconds or interval type with clear unit
- Booleans: use only for truly binary states
- Status: enum/check constraint/status table depending on change frequency
- Text: bounded string when the value has a known max length
- JSON: use for flexible metadata, not for core relational facts that need constraints or joins

## Nullability

Every nullable field needs a reason:

- Unknown
- Not applicable
- Not yet collected
- Cleared by user
- Set only after a lifecycle transition

If these meanings differ, use separate fields or a status model. Avoid nullable fields that force every query to guess the meaning.

## Normalization

Default to normalized models:

- Store each fact once
- Use foreign keys for relationships
- Avoid repeated groups in columns
- Avoid comma-separated IDs

Denormalize only when there is a clear reason:

- Historical snapshot, such as product name and price on an order item
- Performance summary, such as cached count or aggregate
- External integration payload that must be preserved as received

Document denormalized fields and their update/invalidation rules.

## Historical Correctness

Preserve snapshots when later edits must not rewrite history:

- Order item product name and unit price
- Invoice billing address
- Tax rate used for a transaction
- Contract version accepted by a user
- Currency and exchange rate used at transaction time

Do not rely only on current foreign-keyed records when historical documents or financial records must remain accurate.

## State Modeling

For lifecycle state, define:

- Allowed states
- Initial state
- Terminal states
- Legal transitions
- Actor allowed to transition
- Timestamp for important transitions

Use a state field for current state and an event/history table when transition history matters.

## Multi-Tenancy

If data belongs to an organization, workspace, customer, or tenant:

- Add tenant scope to all scoped business tables
- Include tenant scope in unique constraints
- Include tenant scope in indexes used by list queries
- Test that cross-tenant reads and writes are impossible

Retrofitting tenant scope later is expensive; decide early.
