#!/usr/bin/env python3
"""Generic HTTP smoke-test helper for backend APIs."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run HTTP smoke checks against a backend API.")
    parser.add_argument("--base-url", default="", help="Base URL, for example http://localhost:3000")
    parser.add_argument("--case", action="append", default=[], help="JSON case file. Can be repeated.")
    parser.add_argument("--method", default="GET", help="Single-case HTTP method. Default: GET")
    parser.add_argument("--path", default="/", help="Single-case path or full URL. Default: /")
    parser.add_argument("--header", action="append", default=[], help="Header in Name:Value form.")
    parser.add_argument("--body", default=None, help="Raw request body for single-case mode.")
    parser.add_argument("--json", default=None, help="JSON request body for single-case mode.")
    parser.add_argument("--expect-status", type=int, default=200, help="Expected status. Default: 200")
    parser.add_argument("--expect-json", action="append", default=[], help="JSON path expectation path=value.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout seconds. Default: 10")
    parser.add_argument("--out", default="api-verification-report.json", help="Report path.")
    return parser.parse_args()


def headers_from(values: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for raw in values:
        if ":" not in raw:
            raise SystemExit(f"Invalid header {raw!r}. Expected Name:Value.")
        name, value = raw.split(":", 1)
        headers[name.strip()] = value.strip()
    return headers


def load_case(path: str) -> dict[str, Any]:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Failed to read case {path}: {exc}") from exc


def url_for(base_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not base_url:
        return path
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def single_case(args: argparse.Namespace) -> dict[str, Any]:
    headers = headers_from(args.header)
    body: Any = args.body
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


def encode_body(case: dict[str, Any], headers: dict[str, str]) -> bytes | None:
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


def json_path(data: Any, path: str) -> Any:
    if path in {"", "$"}:
        return data
    current = data
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


def expected_value(raw: str) -> Any:
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def run_case(base_url: str, case: dict[str, Any], timeout: float) -> dict[str, Any]:
    method = str(case.get("method", "GET")).upper()
    url = url_for(base_url, str(case.get("path", "/")))
    headers = {str(k): str(v) for k, v in case.get("headers", {}).items()}
    body = encode_body(case, headers)
    expected_status = int(case.get("expectStatus", case.get("expectedStatus", 200)))
    started = time.time()
    result: dict[str, Any] = {
        "name": case.get("name") or case.get("path") or url,
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

    text = raw_body.decode("utf-8", errors="replace")
    result.update(
        {
            "status": status,
            "durationMs": round((time.time() - started) * 1000),
            "responseHeaders": response_headers,
            "responseBodyPreview": text[:2000],
        }
    )
    result["checks"].append({"name": "status", "passed": status == expected_status, "expected": expected_status, "actual": status})

    parsed: Any = None
    content_type = response_headers.get("Content-Type", response_headers.get("content-type", ""))
    if text and (text.strip().startswith(("{", "[")) or "json" in content_type.lower()):
        try:
            parsed = json.loads(text)
            result["json"] = parsed
        except json.JSONDecodeError as exc:
            result["checks"].append({"name": "parse-json", "passed": False, "error": str(exc)})

    for path, expected_raw in case.get("expectJson", {}).items():
        expected = expected_value(str(expected_raw))
        try:
            actual = json_path(parsed, path)
            result["checks"].append({"name": f"json:{path}", "passed": actual == expected, "expected": expected, "actual": actual})
        except Exception as exc:
            result["checks"].append({"name": f"json:{path}", "passed": False, "expected": expected, "error": str(exc)})

    result["passed"] = all(check.get("passed") for check in result["checks"])
    return result


def main() -> int:
    args = parse_args()
    cases = [load_case(path) for path in args.case] if args.case else [single_case(args)]
    results = [run_case(args.base_url, case, args.timeout) for case in cases]
    report = {
        "baseUrl": args.base_url,
        "total": len(results),
        "passed": sum(1 for item in results if item.get("passed")),
        "failed": sum(1 for item in results if not item.get("passed")),
        "results": results,
    }
    report["status"] = "success" if report["failed"] == 0 else "failed"
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": args.out}, indent=2))
    return 0 if report["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
