#!/usr/bin/env python3
"""Project reconnaissance helper for backend API work.

This script scans a repository for backend framework markers, package scripts,
database schema files, auth-related files, route/controller files, and tests. It
does not replace reading code; it gives the agent a structured first pass.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".next",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "target",
    ".gradle",
}


TEXT_SUFFIXES = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".py",
    ".go",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".prisma",
    ".graphql",
    ".gql",
    ".sql",
}

SOURCE_SUFFIXES = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".py",
    ".go",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".prisma",
    ".graphql",
    ".gql",
    ".sql",
}


MARKER_FILES = [
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "manage.py",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Gemfile",
    "composer.json",
    "artisan",
]


FRAMEWORK_MARKERS = {
    "nestjs": ["@nestjs/common", "@Controller", "@Module", "@Injectable"],
    "express": ["express", "Router()", "app.get(", "router.get("],
    "fastify": ["fastify", "FastifyInstance"],
    "koa": ["koa", "koa-router"],
    "next-api": ["pages/api", "app/api"],
    "fastapi": ["FastAPI(", "APIRouter", "Depends("],
    "django": ["django", "rest_framework", "urlpatterns", "ViewSet", "Serializer"],
    "flask": ["Flask(", "Blueprint(", "@app.route", "@bp.route"],
    "spring": ["@RestController", "@RequestMapping", "@GetMapping", "@PostMapping"],
    "go-gin": ["github.com/gin-gonic/gin", "gin.Context"],
    "go-chi": ["github.com/go-chi/chi", "chi.Router"],
    "rails": ["config/routes.rb", "ApplicationController", "ActiveRecord"],
    "laravel": ["Illuminate\\", "routes/api.php", "Controller.php"],
}


ORM_MARKERS = {
    "prisma": ["schema.prisma", "@prisma/client"],
    "typeorm": ["typeorm", "@Entity", "DataSource"],
    "sequelize": ["sequelize", "Sequelize"],
    "mongoose": ["mongoose"],
    "sqlalchemy": ["sqlalchemy", "declarative_base", "mapped_column"],
    "django-orm": ["models.Model"],
    "gorm": ["gorm.io/gorm"],
    "jpa": ["@Entity", "JpaRepository"],
    "active-record": ["ActiveRecord::"],
    "eloquent": ["Illuminate\\Database\\Eloquent"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect a backend project and output a JSON reconnaissance report.")
    parser.add_argument("path", nargs="?", default=".", help="Project root to inspect. Default: current directory.")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan. Default: 5000.")
    parser.add_argument("--max-read-bytes", type=int, default=40000, help="Maximum bytes to read per text file. Default: 40000.")
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def should_skip_path(path: Path) -> bool:
    try:
        skill_root = Path(__file__).resolve().parents[1]
        path.resolve().relative_to(skill_root)
        return True
    except ValueError:
        return False


def iter_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for current_root, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            path = Path(current_root) / name
            if should_skip_path(path):
                continue
            files.append(path)
            if len(files) >= max_files:
                return files
    return files


def read_text_sample(path: Path, max_bytes: int) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="ignore")
    except OSError:
        return ""


def load_package_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def detect_package_manager(files: list[Path]) -> str | None:
    names = {f.name for f in files}
    if "pnpm-lock.yaml" in names:
        return "pnpm"
    if "yarn.lock" in names:
        return "yarn"
    if "package-lock.json" in names:
        return "npm"
    if "package.json" in names:
        return "npm"
    if "uv.lock" in names:
        return "uv"
    if "poetry.lock" in names:
        return "poetry"
    if "Pipfile" in names:
        return "pipenv"
    if "go.mod" in names:
        return "go"
    if "pom.xml" in names:
        return "maven"
    if "build.gradle" in names or "build.gradle.kts" in names:
        return "gradle"
    if "Gemfile" in names:
        return "bundler"
    if "composer.json" in names:
        return "composer"
    return None


def classify_files(files: list[Path], root: Path) -> dict[str, list[str]]:
    categories = {
        "routes": [],
        "controllers": [],
        "resolvers": [],
        "services": [],
        "repositories": [],
        "models": [],
        "migrations": [],
        "schemas": [],
        "auth": [],
        "tests": [],
        "apiDocs": [],
    }
    for path in files:
        if path.suffix.lower() not in SOURCE_SUFFIXES and path.name not in MARKER_FILES:
            continue
        relative = rel(path, root)
        low = relative.lower()
        name = path.name.lower()
        if any(part in low for part in ["route", "routes", "router"]) or "/api/" in low or "\\api\\" in low:
            categories["routes"].append(relative)
        if "controller" in name or "/controllers/" in low:
            categories["controllers"].append(relative)
        if "resolver" in name or "/resolvers/" in low:
            categories["resolvers"].append(relative)
        if "service" in name or "/services/" in low:
            categories["services"].append(relative)
        if "repository" in name or "repo" in name or "/repositories/" in low:
            categories["repositories"].append(relative)
        if "model" in name or "entity" in name or "/models/" in low or "/entities/" in low:
            categories["models"].append(relative)
        if "migration" in low or "/migrations/" in low or "\\migrations\\" in low:
            categories["migrations"].append(relative)
        if path.suffix.lower() in {".prisma", ".graphql", ".gql", ".sql"} or "schema" in name:
            categories["schemas"].append(relative)
        if any(token in low for token in ["auth", "jwt", "session", "permission", "policy", "guard", "passport"]):
            categories["auth"].append(relative)
        if any(token in low for token in ["test", "spec", "__tests__", "/tests/"]):
            categories["tests"].append(relative)
        if any(token in low for token in ["openapi", "swagger", "api-doc", "apidoc"]):
            categories["apiDocs"].append(relative)
    return {key: values[:50] for key, values in categories.items() if values}


def detect_markers(files: list[Path], root: Path, max_read_bytes: int) -> tuple[list[str], list[str]]:
    framework_hits: set[str] = set()
    orm_hits: set[str] = set()
    relative_paths = [rel(path, root) for path in files]
    joined_paths = "\n".join(relative_paths)

    for name, markers in FRAMEWORK_MARKERS.items():
        if any(marker in joined_paths for marker in markers if "/" in marker):
            framework_hits.add(name)

    text_files = [path for path in files if path.suffix.lower() in TEXT_SUFFIXES]
    for path in text_files[:1000]:
        sample = read_text_sample(path, max_read_bytes)
        if not sample:
            continue
        for name, markers in FRAMEWORK_MARKERS.items():
            if any(marker in sample for marker in markers):
                framework_hits.add(name)
        for name, markers in ORM_MARKERS.items():
            if any(marker in sample or marker in path.name for marker in markers):
                orm_hits.add(name)

    return sorted(framework_hits), sorted(orm_hits)


def collect_commands(root: Path) -> dict[str, Any]:
    commands: dict[str, Any] = {}
    package_json = root / "package.json"
    if package_json.exists():
        pkg = load_package_json(package_json)
        scripts = pkg.get("scripts")
        if isinstance(scripts, dict):
            commands["packageScripts"] = scripts

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        text = read_text_sample(pyproject, 60000)
        commands["hasPyproject"] = True
        if "pytest" in text:
            commands["pythonTestHint"] = "pytest"

    if (root / "go.mod").exists():
        commands["goTestHint"] = "go test ./..."
    if (root / "pom.xml").exists():
        commands["mavenTestHint"] = "mvn test"
    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        commands["gradleTestHint"] = "./gradlew test"
    if (root / "Gemfile").exists():
        commands["rubyTestHint"] = "bundle exec rspec or bin/rails test"
    if (root / "composer.json").exists():
        commands["phpTestHint"] = "composer test or vendor/bin/phpunit"
    return commands


def main() -> int:
    args = parse_args()
    root = Path(args.path).resolve()
    files = iter_files(root, args.max_files)
    marker_files = [rel(path, root) for path in files if path.name in MARKER_FILES]
    frameworks, orm = detect_markers(files, root, args.max_read_bytes)
    report = {
        "root": str(root),
        "fileCountScanned": len(files),
        "markerFiles": sorted(marker_files),
        "packageManagerHint": detect_package_manager(files),
        "frameworkHints": frameworks,
        "ormHints": orm,
        "commands": collect_commands(root),
        "notableFiles": classify_files(files, root),
        "notes": [
            "This is a heuristic report. Read the relevant files before editing.",
            "Do not infer database fields, auth rules, or response contracts from this report alone.",
        ],
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
