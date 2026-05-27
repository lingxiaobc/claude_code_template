# Project Recon

Use this file during the Inspect phase. The goal is to ground the implementation in the actual project instead of framework assumptions.

## First Pass

Inspect likely project markers:

- Node/TypeScript: `package.json`, lockfiles, `tsconfig.json`, `src/`, `server/`, `app/`
- Python: `pyproject.toml`, `requirements.txt`, `setup.py`, `Pipfile`, `manage.py`, `app/`
- Go: `go.mod`, `cmd/`, `internal/`, `pkg/`
- Java/Kotlin: `pom.xml`, `build.gradle`, `src/main/`
- Ruby: `Gemfile`, `config/routes.rb`, `app/controllers/`
- PHP: `composer.json`, `artisan`, `routes/`, `app/Http/Controllers/`

Use `scripts/inspect_backend.py` for a first pass, then read the files it reports. Treat the script as a triage helper, not a replacement for reading code.

## Identify the Framework

Look for framework-specific evidence:

- Express/Fastify/Koa: route registration, middleware, `app.get`, `router.post`
- NestJS: modules, controllers, providers, decorators such as `@Controller`
- Next.js API routes: `pages/api`, `app/api`
- FastAPI: `FastAPI()`, `APIRouter`, Pydantic models
- Django/DRF: `urls.py`, views, serializers, viewsets
- Flask: `Flask()`, blueprints, route decorators
- Spring: `@RestController`, `@RequestMapping`, services, repositories
- Go: chi/gin/echo/fiber/http handlers
- Rails: routes, controllers, models, serializers
- Laravel: routes, controllers, requests, resources

Do not write framework-specific code until the framework is confirmed.

## Find Existing API Patterns

Find endpoints similar to the requested work:

- Same resource type
- Same auth/permission pattern
- Same request validation style
- Same pagination/filtering/sorting style
- Same error handling style
- Same database access style
- Same test style

Nearby code is the strongest reference. Prefer matching it over generic best practices.

## Find Data Sources

Confirm database shape from authoritative sources:

- ORM schema: Prisma, TypeORM entity, Sequelize model, SQLAlchemy model, Django model, GORM model, JPA entity
- Migrations
- SQL schema files
- GraphQL schema
- OpenAPI schema
- Existing repository/query code

If a field, relation, enum, or table cannot be found, do not invent it.

## Find Auth and Permissions

Locate:

- Authentication middleware, guards, decorators, dependencies, or filters
- Current user/session extraction
- Role, permission, tenant, organization, or ownership checks
- Existing unauthorized and forbidden error behavior
- Test helpers for authenticated requests

Writing endpoints without confirmed auth behavior is risky. Ask the user if auth requirements are ambiguous.

## Find Commands

Read existing scripts before running commands:

- Dev server
- Test
- Integration/e2e test
- Build/compile
- Type check
- Lint
- Format check
- OpenAPI/schema generation
- Database migration/test setup

Use repo scripts instead of inventing commands.
