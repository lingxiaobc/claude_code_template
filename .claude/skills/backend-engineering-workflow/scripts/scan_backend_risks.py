#!/usr/bin/env python3
"""Static backend risk scanner.

This is a lightweight heuristic scanner for common backend risk patterns. It is
not a security tool and does not prove safety; use findings as review prompts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


SKIP_DIRS = {".git", "node_modules", "dist", "build", "coverage", ".venv", "venv", "__pycache__", "target"}
SOURCE_SUFFIXES = {".js", ".jsx", ".ts", ".tsx", ".py", ".go", ".java", ".kt", ".rb", ".php", ".sql", ".env", ".yml", ".yaml"}

RULES = [
    ("possible-hardcoded-secret", "high", re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{12,}['\"]")),
    ("disabled-tls-verification", "high", re.compile(r"(?i)(rejectUnauthorized\s*:\s*false|verify\s*=\s*False|insecure_skip_verify|CURLOPT_SSL_VERIFYPEER\s*,\s*0)")),
    ("possible-sql-string-interpolation", "high", re.compile(r"(?i)(select|insert|update|delete).*(\$\{|%s|f['\"]|format\(|\+)", re.DOTALL)),
    ("wildcard-cors", "medium", re.compile(r"(?i)(cors|Access-Control-Allow-Origin).*(\*|origin\s*:\s*true)")),
    ("raw-exec", "medium", re.compile(r"(?i)(exec\(|execSync\(|subprocess\.(Popen|run|call)|os\.system\()")),
    ("todo-or-fixme", "low", re.compile(r"(?i)\b(TODO|FIXME|HACK)\b")),
    ("debug-print", "low", re.compile(r"\b(console\.log|print\(|System\.out\.println|fmt\.Println)\b")),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan backend source files for common risk patterns.")
    parser.add_argument("path", nargs="?", default=".", help="Project root. Default: current directory.")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan. Default: 5000.")
    parser.add_argument("--out", default="", help="Optional JSON report path.")
    return parser.parse_args()


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
            if path.suffix.lower() in SOURCE_SUFFIXES or path.name.startswith(".env"):
                files.append(path)
                if len(files) >= max_files:
                    return files
    return files


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def scan_file(path: Path, root: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []
    findings: list[dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        for rule, severity, pattern in RULES:
            if pattern.search(line):
                findings.append(
                    {
                        "file": rel(path, root),
                        "line": index,
                        "rule": rule,
                        "severity": severity,
                        "preview": line.strip()[:200],
                    }
                )
    return findings


def main() -> int:
    args = parse_args()
    root = Path(args.path).resolve()
    findings: list[dict[str, Any]] = []
    for path in iter_files(root, args.max_files):
        findings.extend(scan_file(path, root))
    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda item: (severity_order.get(item["severity"], 9), item["file"], item["line"]))
    report = {
        "root": str(root),
        "totalFindings": len(findings),
        "findings": findings,
        "notes": ["Heuristic scan only. Review findings manually before changing code."],
    }
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if any(item["severity"] == "high" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
