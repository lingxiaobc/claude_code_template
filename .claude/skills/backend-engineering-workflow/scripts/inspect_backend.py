#!/usr/bin/env python3
"""Backend project reconnaissance helper.

Scans a repository for backend framework markers, package scripts, route files,
models, migrations, auth files, tests, and API docs. This is a heuristic first
pass; agents must still read relevant files before editing.
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
    ".json",
    ".toml",
    ".yaml",
    ".yml",
}

MARKER_FILES = {
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
    "manage.py",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Gemfile",
    "composer.json",
    "artisan",
}

FRAMEWORK_MARKERS = {
    "nestjs": ["@nestjs/common", "@Controller", "@Module", "@Injectable"],
    "express": ["from 'express'", 'from "express"', "require('express')", 'require("express")', "express.Router"],
    "fastify": ["from 'fastify'", 'from "fastify"', "require('fastify')", "FastifyInstance"],
    "koa": ["from 'koa'", 'from "koa"', "require('koa')"],
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
    parser = argparse.ArgumentParser(description="Inspect a backend project and output JSON.")
    parser.add_argument("path", nargs="?", default=".", help="Project root to inspect. Default: current directory.")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan. Default: 5000.")
    parser.add_argument("--max-read-bytes", type=int, default=40000, help="Maximum bytes to read per file. Default: 40000.")
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def inside_bundled_backend_skill(path: Path) -> bool:
    try:
        resolved = path.resolve()
        this_skill = Path(__file__).resolve().parents[1]
        resolved.relative_to(this_skill)
        return True
    except ValueError:
        return False


def iter_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for current_root, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            path = Path(current_root) / name
            if inside_bundled_backend_skill(path):
                continue
            files.append(path)
            if len(files) >= max_files:
                return files
    return files


def read_sample(path: Path, max_bytes: int) -> str:
    try:
        return path.read_bytes()[:max_bytes].decode("utf-8", errors="ignore")
    except OSError:
        return ""


def package_manager(files: list[Path]) -> str | None:
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


def package_scripts(root: Path) -> dict[str, str]:
    path = root / "package.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    scripts = data.get("scripts", {})
    return scripts if isinstance(scripts, dict) else {}


def detect_markers(files: list[Path], root: Path, max_read_bytes: int) -> tuple[list[str], list[str]]:
    framework_hits: set[str] = set()
    orm_hits: set[str] = set()
    path_text = "\n".join(rel(f, root) for f in files)

    for name, markers in FRAMEWORK_MARKERS.items():
        if any("/" in marker and marker in path_text for marker in markers):
            framework_hits.add(name)

    for path in files:
        if path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        sample = read_sample(path, max_read_bytes)
        if not sample:
            continue
        for name, markers in FRAMEWORK_MARKERS.items():
            if any(marker in sample for marker in markers):
                framework_hits.add(name)
        for name, markers in ORM_MARKERS.items():
            if any(marker in sample or marker in path.name for marker in markers):
                orm_hits.add(name)

    return sorted(framework_hits), sorted(orm_hits)


def classify(files: list[Path], root: Path) -> dict[str, list[str]]:
    categories: dict[str, list[str]] = {
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
        "config": [],
    }
    for path in files:
        if path.suffix.lower() not in SOURCE_SUFFIXES and path.name not in MARKER_FILES:
            continue
        relative = rel(path, root)
        low = relative.lower()
        name = path.name.lower()
        if any(token in low for token in ["route", "routes", "router", "/api/"]):
            categories["routes"].append(relative)
        if "controller" in name or "/controllers/" in low:
            categories["controllers"].append(relative)
        if "resolver" in name or "/resolvers/" in low:
            categories["resolvers"].append(relative)
        if "service" in name or "/services/" in low:
            categories["services"].append(relative)
        if "repository" in name or "/repositories/" in low:
            categories["repositories"].append(relative)
        if any(token in low for token in ["model", "entity", "/models/", "/entities/"]):
            categories["models"].append(relative)
        if "migration" in low or "/migrations/" in low:
            categories["migrations"].append(relative)
        if path.suffix.lower() in {".prisma", ".graphql", ".gql", ".sql"} or "schema" in name:
            categories["schemas"].append(relative)
        if any(token in low for token in ["auth", "jwt", "session", "permission", "policy", "guard", "passport"]):
            categories["auth"].append(relative)
        if any(token in low for token in ["test", "spec", "__tests__", "/tests/"]):
            categories["tests"].append(relative)
        if any(token in low for token in ["openapi", "swagger", "api-doc", "apidoc", "graphql"]):
            categories["apiDocs"].append(relative)
        if path.name in MARKER_FILES or any(token in low for token in ["config", ".env.example"]):
            categories["config"].append(relative)
    return {key: values[:80] for key, values in categories.items() if values}


def command_hints(root: Path, files: list[Path]) -> dict[str, Any]:
    hints: dict[str, Any] = {}
    scripts = package_scripts(root)
    if scripts:
        hints["packageScripts"] = scripts
    names = {f.name for f in files}
    if "pyproject.toml" in names or "requirements.txt" in names:
        hints["pythonTestHint"] = "pytest (if configured)"
    if "go.mod" in names:
        hints["goTestHint"] = "go test ./..."
    if "pom.xml" in names:
        hints["mavenTestHint"] = "mvn test"
    if "build.gradle" in names or "build.gradle.kts" in names:
        hints["gradleTestHint"] = "./gradlew test"
    if "Gemfile" in names:
        hints["rubyTestHint"] = "bundle exec rspec or bin/rails test"
    if "composer.json" in names:
        hints["phpTestHint"] = "composer test or vendor/bin/phpunit"
    return hints


def main() -> int:
    args = parse_args()
    root = Path(args.path).resolve()
    files = iter_files(root, args.max_files)
    frameworks, orm = detect_markers(files, root, args.max_read_bytes)
    report = {
        "root": str(root),
        "fileCountScanned": len(files),
        "markerFiles": sorted(rel(f, root) for f in files if f.name in MARKER_FILES),
        "packageManagerHint": package_manager(files),
        "frameworkHints": frameworks,
        "ormHints": orm,
        "commands": command_hints(root, files),
        "notableFiles": classify(files, root),
        "notes": [
            "This is heuristic. Read relevant files before editing.",
            "Do not infer database fields, auth rules, or contracts from this report alone.",
        ],
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
