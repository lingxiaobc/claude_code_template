#!/usr/bin/env python3
"""Inspect a project for database schema, migration, and query artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    ".venv",
    "venv",
    "__pycache__",
    "target",
    "vendor",
}

TEXT_SUFFIXES = {
    ".sql",
    ".prisma",
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".rb",
    ".go",
    ".java",
    ".kt",
    ".cs",
    ".php",
    ".rs",
    ".ex",
    ".exs",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
    ".env",
}

SCHEMA_NAME_PATTERNS = [
    re.compile(r"(^|/)schema\.(sql|prisma|rb|ts|js|py)$"),
    re.compile(r"(^|/)models?(/|$)"),
    re.compile(r"(^|/)entities?(/|$)"),
    re.compile(r"(^|/)db/schema\.rb$"),
    re.compile(r"(^|/)src/db/schema\.(ts|js)$"),
]

MIGRATION_PATH_PATTERNS = [
    re.compile(r"(^|/)migrations?(/|$)"),
    re.compile(r"(^|/)db/migrate(/|$)"),
    re.compile(r"(^|/)alembic/versions(/|$)"),
    re.compile(r"(^|/)flyway(/|$)"),
    re.compile(r"(^|/)liquibase(/|$)"),
    re.compile(r"(^|/)db/changelog(/|$)"),
]

SEED_PATH_PATTERNS = [
    re.compile(r"(^|/)(seeds?|fixtures?|factories?)(/|$)"),
    re.compile(r"(^|/)db/seeds\.(rb|sql|ts|js|py)$"),
]

QUERY_PATH_PATTERNS = [
    re.compile(r"(^|/)(repositories?|dao|queries|services?)(/|$)"),
    re.compile(r"(^|/).*query.*\.(sql|ts|js|py|rb|go|java|cs|php)$"),
]

DB_CONFIG_NAMES = {
    "prisma.schema",
    "schema.prisma",
    "drizzle.config.ts",
    "drizzle.config.js",
    "drizzle.config.mjs",
    "knexfile.js",
    "knexfile.ts",
    "sequelize.config.js",
    "typeorm.config.ts",
    "typeorm.config.js",
    "database.yml",
    "alembic.ini",
    "liquibase.properties",
    "flyway.conf",
    "hibernate.cfg.xml",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report database-related project artifacts as JSON.")
    parser.add_argument("path", nargs="?", default=".", help="Project root. Default: current directory.")
    parser.add_argument("--max-files", type=int, default=8000, help="Maximum files to inspect. Default: 8000.")
    parser.add_argument("--out", default="", help="Optional JSON report path.")
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def iter_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for current_root, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            path = Path(current_root) / name
            if path.suffix.lower() in TEXT_SUFFIXES or path.name in DB_CONFIG_NAMES or path.name.startswith(".env"):
                files.append(path)
                if len(files) >= max_files:
                    return files
    return files


def read_small_text(path: Path, limit: int = 200_000) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def add_detected(detected: dict[str, set[str]], tech: str, evidence: str) -> None:
    detected.setdefault(tech, set()).add(evidence)


def detect_from_path(path: Path, root: Path, detected: dict[str, set[str]]) -> None:
    p = rel(path, root)
    low = p.lower()
    name = path.name.lower()
    if "schema.prisma" in low:
        add_detected(detected, "Prisma", p)
    if "drizzle.config" in name or "drizzle/" in low:
        add_detected(detected, "Drizzle", p)
    if "knexfile" in name:
        add_detected(detected, "Knex", p)
    if "sequelize" in low:
        add_detected(detected, "Sequelize", p)
    if "typeorm" in low:
        add_detected(detected, "TypeORM", p)
    if "alembic" in low or name == "alembic.ini":
        add_detected(detected, "Alembic", p)
    if "db/schema.rb" in low or "db/migrate" in low:
        add_detected(detected, "Rails ActiveRecord", p)
    if name == "models.py" or "/models/" in low:
        add_detected(detected, "Django or SQLAlchemy models", p)
    if "liquibase" in low or "changelog" in low:
        add_detected(detected, "Liquibase", p)
    if "flyway" in low:
        add_detected(detected, "Flyway", p)
    if path.suffix.lower() == ".sql":
        add_detected(detected, "SQL files", p)


def detect_from_package_json(path: Path, root: Path, detected: dict[str, set[str]], commands: dict[str, str]) -> None:
    content = read_small_text(path)
    if not content:
        return
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return
    deps: dict[str, Any] = {}
    for section in ("dependencies", "devDependencies", "peerDependencies"):
        value = data.get(section)
        if isinstance(value, dict):
            deps.update(value)
    dependency_map = {
        "prisma": "Prisma",
        "@prisma/client": "Prisma",
        "drizzle-orm": "Drizzle",
        "knex": "Knex",
        "sequelize": "Sequelize",
        "typeorm": "TypeORM",
        "pg": "PostgreSQL driver",
        "mysql2": "MySQL driver",
        "sqlite3": "SQLite driver",
        "better-sqlite3": "SQLite driver",
        "mssql": "SQL Server driver",
    }
    for dep, tech in dependency_map.items():
        if dep in deps:
            add_detected(detected, tech, f"{rel(path, root)} dependency {dep}")
    scripts = data.get("scripts")
    if isinstance(scripts, dict):
        for name, command in scripts.items():
            if re.search(r"(?i)(db|database|migrat|prisma|drizzle|schema|seed)", name + " " + str(command)):
                commands[name] = str(command)


def detect_from_python_config(path: Path, root: Path, detected: dict[str, set[str]]) -> None:
    content = read_small_text(path)
    low = content.lower()
    checks = {
        "sqlalchemy": "SQLAlchemy",
        "alembic": "Alembic",
        "django": "Django ORM",
        "psycopg": "PostgreSQL driver",
        "asyncpg": "PostgreSQL driver",
        "mysqlclient": "MySQL driver",
        "pymysql": "MySQL driver",
    }
    for marker, tech in checks.items():
        if marker in low:
            add_detected(detected, tech, f"{rel(path, root)} mentions {marker}")


def classify(path: Path, root: Path) -> dict[str, bool]:
    p = rel(path, root).replace("\\", "/")
    low = p.lower()
    return {
        "schema": path.name.lower() in DB_CONFIG_NAMES or any(pattern.search(low) for pattern in SCHEMA_NAME_PATTERNS),
        "migration": any(pattern.search(low) for pattern in MIGRATION_PATH_PATTERNS),
        "seed": any(pattern.search(low) for pattern in SEED_PATH_PATTERNS),
        "query": path.suffix.lower() == ".sql" or any(pattern.search(low) for pattern in QUERY_PATH_PATTERNS),
        "config": path.name in DB_CONFIG_NAMES or path.name.lower() in {"package.json", "pyproject.toml", "requirements.txt", "gemfile", "go.mod", "composer.json"},
    }


def collect_env_hints(root: Path) -> list[str]:
    hints: set[str] = set()
    for name in (".env", ".env.example", ".env.local", ".env.development", ".env.test"):
        path = root / name
        if not path.exists():
            continue
        for line in read_small_text(path, 50_000).splitlines():
            if "=" not in line:
                continue
            key = line.split("=", 1)[0].strip()
            if re.search(r"(?i)(database|db_|postgres|mysql|sqlite|mongo|redis|dsn|connection)", key):
                hints.add(f"{name}:{key}")
    return sorted(hints)


def main() -> int:
    args = parse_args()
    root = Path(args.path).resolve()
    files = iter_files(root, args.max_files)
    detected: dict[str, set[str]] = {}
    commands: dict[str, str] = {}
    schema_files: list[str] = []
    migration_files: list[str] = []
    seed_files: list[str] = []
    query_files: list[str] = []
    config_files: list[str] = []

    for path in files:
        detect_from_path(path, root, detected)
        if path.name.lower() == "package.json":
            detect_from_package_json(path, root, detected, commands)
        if path.name.lower() in {"pyproject.toml", "requirements.txt", "setup.py"}:
            detect_from_python_config(path, root, detected)
        classes = classify(path, root)
        p = rel(path, root)
        if classes["schema"]:
            schema_files.append(p)
        if classes["migration"]:
            migration_files.append(p)
        if classes["seed"]:
            seed_files.append(p)
        if classes["query"]:
            query_files.append(p)
        if classes["config"]:
            config_files.append(p)

    report = {
        "root": str(root),
        "filesInspected": len(files),
        "detectedTechnologies": [
            {"name": name, "evidence": sorted(evidence)[:12]}
            for name, evidence in sorted(detected.items())
        ],
        "configFiles": sorted(set(config_files))[:100],
        "schemaFiles": sorted(set(schema_files))[:150],
        "migrationFiles": sorted(set(migration_files))[:200],
        "seedOrFixtureFiles": sorted(set(seed_files))[:100],
        "queryRelatedFiles": sorted(set(query_files))[:200],
        "possibleDatabaseEnvKeys": collect_env_hints(root),
        "packageScripts": commands,
        "notes": [
            "This is a heuristic reconnaissance report.",
            "Read the reported schema, migration, and query files before changing database behavior.",
        ],
    }
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
