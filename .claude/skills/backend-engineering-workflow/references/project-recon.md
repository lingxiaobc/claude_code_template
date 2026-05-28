# Project Recon

Use this during the Inspect phase.

## Goals

Establish facts before implementation:

- Language and runtime
- Backend framework
- Package manager and commands
- App entrypoint
- Route/controller/resolver layout
- Service, repository, and model layers
- Database and ORM
- Auth and permission model
- Error handling
- Logging and observability
- Tests and fixtures
- API docs or schema generation

## First Files To Inspect

Common markers:

- Node: `package.json`, lockfiles, `tsconfig.json`, `src/`, `server/`
- Python: `pyproject.toml`, `requirements.txt`, `manage.py`, `app/`
- Go: `go.mod`, `cmd/`, `internal/`
- Java/Kotlin: `pom.xml`, `build.gradle`, `src/main/`
- Ruby: `Gemfile`, `config/routes.rb`, `app/controllers/`
- PHP: `composer.json`, `artisan`, `routes/`, `app/Http/Controllers/`

Run `scripts/inspect_backend.py` for a first-pass JSON report, then read relevant files manually.

## Framework Evidence

Confirm framework from code, not assumptions:

- Express/Fastify/Koa: route registration, middleware, `app.get`, `router.post`
- NestJS: modules, controllers, providers, decorators
- Next.js API routes: `pages/api`, `app/api`
- FastAPI: `FastAPI`, `APIRouter`, Pydantic models
- Django/DRF: `urls.py`, views, serializers, viewsets
- Flask: blueprints and route decorators
- Spring: `@RestController`, `@RequestMapping`, repositories
- Go: chi, gin, echo, fiber, or standard `net/http`
- Rails: routes, controllers, ActiveRecord models
- Laravel: routes, controllers, requests, resources

## Local Pattern Search

Find similar code before creating new patterns:

- Similar endpoint or resource
- Similar service method
- Similar repository query
- Similar validation schema
- Similar auth requirement
- Similar test case
- Similar error behavior

Nearby code is usually more reliable than generic best practices.

## Data Sources

Confirm data shape from authoritative sources:

- ORM schema such as Prisma, TypeORM entity, Sequelize model, SQLAlchemy model, Django model, GORM model, or JPA entity
- Migrations
- SQL schema files
- GraphQL schema
- OpenAPI schema
- Existing repository or query code

If a field, relation, enum, table, or cascade behavior cannot be found, do not invent it.

## Auth And Permissions

Locate:

- Authentication middleware, guards, decorators, dependencies, or filters
- Current-user or session extraction
- Role, permission, tenant, organization, or ownership checks
- Existing unauthorized and forbidden error behavior
- Test helpers for authenticated requests

Writing endpoints without confirmed auth behavior is risky. Ask the user if auth requirements are ambiguous and the endpoint writes or exposes sensitive data.

## Commands

Identify commands from project files:

- Dev server
- Typecheck or compile
- Lint
- Unit tests
- Integration/e2e tests
- Build
- Migrations
- Schema generation

Do not invent commands when repo scripts exist.
