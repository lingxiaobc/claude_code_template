#!/usr/bin/env python3
"""Scan schema, migration, and query files for common database risk patterns."""

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

SOURCE_SUFFIXES = {
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
}

LINE_RULES = [
    (
        "money-or-quantity-uses-float",
        "high",
        re.compile(r"(?i)\b(amount|price|cost|balance|subtotal|total|fee|tax|salary|quantity|rate)\b.*\b(float|double precision|double|real)\b"),
        "Financial and precise quantities should use decimal or integer minor units, not floating point.",
    ),
    (
        "update-without-where-review",
        "high",
        re.compile(r"(?i)^\s*update\s+[a-zA-Z0-9_.\"`]+(?!.*\bwhere\b).*$"),
        "UPDATE without WHERE may affect every row. Confirm this is intentional.",
    ),
    (
        "delete-without-where-review",
        "high",
        re.compile(r"(?i)^\s*delete\s+from\s+[a-zA-Z0-9_.\"`]+(?!.*\bwhere\b).*$"),
        "DELETE without WHERE may remove every row. Confirm this is intentional.",
    ),
    (
        "drop-or-truncate-review",
        "high",
        re.compile(r"(?i)\b(drop\s+table|truncate\s+table|drop\s+column)\b"),
        "Destructive schema/data operation. Confirm migration safety and rollback/forward-fix plan.",
    ),
    (
        "raw-sql-string-interpolation",
        "high",
        re.compile(r"(?i)(select|insert|update|delete).*(\$\{|%s|f['\"]|\.format\(|\+)", re.DOTALL),
        "Possible raw SQL string interpolation. Use parameters for values and allowlists for identifiers.",
    ),
    (
        "select-star-review",
        "medium",
        re.compile(r"(?i)\bselect\s+\*\s+from\b"),
        "SELECT * can overfetch and make schema evolution riskier. Select needed columns for production queries.",
    ),
    (
        "cascade-delete-review",
        "medium",
        re.compile(r"(?i)\bon\s+delete\s+cascade\b|onDelete:\s*Cascade"),
        "Cascade delete can remove related data. Confirm it is correct for historical/audit records.",
    ),
    (
        "password-column-review",
        "medium",
        re.compile(r"(?i)\b(password|passwd|pwd)\b(?!.*hash)"),
        "Password-like field without 'hash' in the name. Confirm plaintext passwords are not stored.",
    ),
    (
        "timestamp-without-timezone-review",
        "low",
        re.compile(r"(?i)\btimestamp\b(?![^,\n;]*\b(time\s+zone|timestamptz)\b)"),
        "Timestamp without explicit timezone. Confirm this matches the project convention.",
    ),
    (
        "json-column-review",
        "low",
        re.compile(r"(?i)\b(json|jsonb)\b"),
        "JSON column found. Confirm core relational facts needing constraints are not hidden in JSON.",
    ),
]

CREATE_TABLE_RE = re.compile(
    r"(?is)\bcreate\s+table\s+(?:if\s+not\s+exists\s+)?([a-zA-Z0-9_.\"`]+)\s*\((.*?)\)\s*;",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan database-related files for common risk patterns.")
    parser.add_argument("path", nargs="?", default=".", help="Project root. Default: current directory.")
    parser.add_argument("--max-files", type=int, default=8000, help="Maximum files to scan. Default: 8000.")
    parser.add_argument("--out", default="", help="Optional JSON report path.")
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def inside_this_skill(path: Path) -> bool:
    try:
        path.resolve().relative_to(Path(__file__).resolve().parents[1])
        return True
    except ValueError:
        return False


def iter_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for current_root, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            path = Path(current_root) / name
            if inside_this_skill(path):
                continue
            if path.suffix.lower() in SOURCE_SUFFIXES or name in {"schema.prisma", "package.json", "pyproject.toml"}:
                files.append(path)
                if len(files) >= max_files:
                    return files
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def line_findings(path: Path, root: Path, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for index, line in enumerate(text.splitlines(), start=1):
        for rule, severity, pattern, detail in LINE_RULES:
            if pattern.search(line):
                findings.append(
                    {
                        "file": rel(path, root),
                        "line": index,
                        "rule": rule,
                        "severity": severity,
                        "detail": detail,
                        "preview": line.strip()[:220],
                    }
                )
    return findings


def create_table_findings(path: Path, root: Path, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if path.suffix.lower() != ".sql":
        return findings
    for match in CREATE_TABLE_RE.finditer(text):
        table_name = match.group(1)
        body = match.group(2)
        start_line = text[: match.start()].count("\n") + 1
        if not re.search(r"(?i)\bprimary\s+key\b", body):
            findings.append(
                {
                    "file": rel(path, root),
                    "line": start_line,
                    "rule": "create-table-without-primary-key",
                    "severity": "high",
                    "detail": "Table definition has no PRIMARY KEY. Confirm this is intentional.",
                    "preview": f"CREATE TABLE {table_name}",
                }
            )
        if re.search(r"(?i)\btenant_id\b", body) and not re.search(r"(?i)\btenant_id\b.*\bnot\s+null\b", body):
            findings.append(
                {
                    "file": rel(path, root),
                    "line": start_line,
                    "rule": "nullable-tenant-scope-review",
                    "severity": "medium",
                    "detail": "tenant_id appears in the table body. Confirm tenant scope is required and indexed.",
                    "preview": f"CREATE TABLE {table_name}",
                }
            )
    return findings


def summarize(findings: list[dict[str, Any]]) -> dict[str, int]:
    summary = {"high": 0, "medium": 0, "low": 0}
    for item in findings:
        severity = item.get("severity")
        if severity in summary:
            summary[severity] += 1
    return summary


def main() -> int:
    args = parse_args()
    root = Path(args.path).resolve()
    findings: list[dict[str, Any]] = []
    for path in iter_files(root, args.max_files):
        text = read_text(path)
        if not text:
            continue
        findings.extend(line_findings(path, root, text))
        findings.extend(create_table_findings(path, root, text))

    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda item: (severity_order.get(item["severity"], 9), item["file"], item["line"], item["rule"]))
    report = {
        "root": str(root),
        "summary": summarize(findings),
        "totalFindings": len(findings),
        "findings": findings,
        "notes": [
            "Heuristic scan only. Findings are review prompts, not proof of defects.",
            "False positives are expected; review against project conventions and database engine behavior.",
        ],
    }
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if report["summary"]["high"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
