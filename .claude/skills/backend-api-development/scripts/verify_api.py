#!/usr/bin/env python3
"""Generic HTTP smoke-test helper for backend API work.

Cases can be supplied as JSON files. The script verifies status code and basic
JSON response fields without depending on third-party packages.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run generic HTTP smoke checks against a backend API.")
    parser.add_argument("--base-url", default="", help="Base URL, for example http://localhost:3000")
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        help="Path to a JSON case file. Can be repeated. If omitted, use --method/--path options.",
    )
    parser.add_argument("--method", default="GET", help="HTTP method for single-case mode. Default: GET")
    parser.add_argument("--path", default="/", help="Path or full URL for single-case mode. Default: /")
    parser.add_argument("--header", action="append", default=[], help="Header in Name:Value form. Can be repeated.")
    parser.add_argument("--body", default=None, help="Raw request body for single-case mode.")
    parser.add_argument("--json", default=None, help="JSON request body for single-case mode.")
    parser.add_argument("--expect-status", type=int, default=200, help="Expected status in single-case mode. Default: 200")
    parser.add_argument("--expect-json", action="append", default=[], help="JSON path expectation in path=value form.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds. Default: 10")
    parser.add_argument("--out", default="api-verification-report.json", help="Report path. Default: api-verification-report.json")
    return parser.parse_args()


def parse_headers(values: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for raw in values:
        if ":" not in raw:
            raise SystemExit(f"Invalid header {raw!r}. Expected Name:Value.")
        name, value = raw.split(":", 1)
        headers[name.strip()] = value.strip()
    return headers


def load_case(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Failed to read case file {path}: {exc}") from exc


def build_url(base_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not base_url:
        return path
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def get_json_path(data: Any, path: str) -> Any:
    current = data
    if path in {"", "$"}:
        return current
    parts = path[2:].split(".") if path.startswith("$.") else path.split(".")
    for part in parts:
        if part == "":
            continue
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(path)
    return current


def coerce_expected(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def make_single_case(args: argparse.Namespace) -> dict[str, Any]:
    body: Any = args.body
    headers = parse_headers(args.header)
    if args.json is not None:
        body = json.loads(args.json)
        headers.setdefault("Content-Type", "application/json")
    return {
        "name": "single-case",
        "method": args.method,
        "path": args.path,
        "headers": headers,
        "body": body,
        "expectStatus": args.expect_status,
        "expectJson": dict(item.split("=", 1) for item in args.expect_json),
    }


def prepare_body(case: dict[str, Any], headers: dict[str, str]) -> bytes | None:
    if "json" in case:
        headers.setdefault("Content-Type", "application/json")
        return json.dumps(case["json"]).encode("utf-8")
    if "body" not in case or case["body"] is None:
        return None
    body = case["body"]
    if isinstance(body, (dict, list)):
        headers.setdefault("Content-Type", "application/json")
        return json.dumps(body).encode("utf-8")
    if isinstance(body, str):
        return body.encode("utf-8")
    return json.dumps(body).encode("utf-8")


def run_case(base_url: str, case: dict[str, Any], timeout: float) -> dict[str, Any]:
    name = case.get("name") or case.get("path") or "case"
    method = str(case.get("method", "GET")).upper()
    url = build_url(base_url, str(case.get("path", "/")))
    headers = {str(k): str(v) for k, v in case.get("headers", {}).items()}
    body = prepare_body(case, headers)
    expected_status = int(case.get("expectStatus", case.get("expectedStatus", 200)))
    started = time.time()
    result: dict[str, Any] = {
        "name": name,
        "method": method,
        "url": url,
        "expectedStatus": expected_status,
        "passed": False,
        "checks": [],
    }

    request = urllib.request.Request(url=url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            raw_body = response.read()
            response_headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        status = exc.code
        raw_body = exc.read()
        response_headers = dict(exc.headers.items())
    except urllib.error.URLError as exc:
        result["error"] = str(exc)
        result["durationMs"] = round((time.time() - started) * 1000)
        return result

    duration_ms = round((time.time() - started) * 1000)
    text = raw_body.decode("utf-8", errors="replace")
    result.update(
        {
            "status": status,
            "durationMs": duration_ms,
            "responseHeaders": response_headers,
            "responseBodyPreview": text[:2000],
        }
    )

    status_passed = status == expected_status
    result["checks"].append(
        {
            "name": "status",
            "passed": status_passed,
            "expected": expected_status,
            "actual": status,
        }
    )

    parsed_json: Any = None
    content_type = response_headers.get("Content-Type", response_headers.get("content-type", ""))
    if text and ("json" in content_type or text.strip().startswith(("{", "["))):
        try:
            parsed_json = json.loads(text)
            result["json"] = parsed_json
        except json.JSONDecodeError as exc:
            result["checks"].append({"name": "parse-json", "passed": False, "error": str(exc)})

    for path, expected_raw in case.get("expectJson", {}).items():
        expected = coerce_expected(str(expected_raw))
        try:
            actual = get_json_path(parsed_json, path)
            passed = actual == expected
            result["checks"].append(
                {
                    "name": f"json:{path}",
                    "passed": passed,
                    "expected": expected,
                    "actual": actual,
                }
            )
        except Exception as exc:
            result["checks"].append(
                {
                    "name": f"json:{path}",
                    "passed": False,
                    "expected": expected,
                    "error": str(exc),
                }
            )

    result["passed"] = all(check.get("passed") for check in result["checks"])
    return result


def main() -> int:
    args = parse_args()
    cases = [load_case(Path(path)) for path in args.case] if args.case else [make_single_case(args)]
    results = [run_case(args.base_url, case, args.timeout) for case in cases]
    report = {
        "baseUrl": args.base_url,
        "total": len(results),
        "passed": sum(1 for result in results if result.get("passed")),
        "failed": sum(1 for result in results if not result.get("passed")),
        "results": results,
    }
    report["status"] = "success" if report["failed"] == 0 else "failed"
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": args.out}, indent=2))
    return 0 if report["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
