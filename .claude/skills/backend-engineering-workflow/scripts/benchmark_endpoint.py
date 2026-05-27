#!/usr/bin/env python3
"""Simple endpoint latency benchmark.

Use for lightweight before/after checks during optimization. This is not a load
testing tool.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a simple HTTP latency benchmark.")
    parser.add_argument("url", help="Full URL to benchmark.")
    parser.add_argument("--method", default="GET", help="HTTP method. Default: GET")
    parser.add_argument("--header", action="append", default=[], help="Header in Name:Value form.")
    parser.add_argument("--body", default=None, help="Raw request body.")
    parser.add_argument("--requests", type=int, default=20, help="Number of requests. Default: 20")
    parser.add_argument("--warmup", type=int, default=2, help="Warmup requests. Default: 2")
    parser.add_argument("--timeout", type=float, default=10.0, help="Timeout seconds. Default: 10")
    parser.add_argument("--out", default="", help="Optional JSON report path.")
    return parser.parse_args()


def parse_headers(values: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for raw in values:
        if ":" not in raw:
            raise SystemExit(f"Invalid header {raw!r}. Expected Name:Value.")
        name, value = raw.split(":", 1)
        headers[name.strip()] = value.strip()
    return headers


def request_once(url: str, method: str, headers: dict[str, str], body: str | None, timeout: float) -> dict[str, Any]:
    data = body.encode("utf-8") if body is not None else None
    request = urllib.request.Request(url=url, data=data, headers=headers, method=method.upper())
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response.read()
            status = response.status
            ok = True
            error = None
    except urllib.error.HTTPError as exc:
        exc.read()
        status = exc.code
        ok = False
        error = str(exc)
    except urllib.error.URLError as exc:
        status = None
        ok = False
        error = str(exc)
    elapsed_ms = (time.perf_counter() - started) * 1000
    return {"durationMs": elapsed_ms, "status": status, "ok": ok, "error": error}


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((pct / 100) * (len(ordered) - 1))))
    return ordered[index]


def main() -> int:
    args = parse_args()
    headers = parse_headers(args.header)
    for _ in range(max(0, args.warmup)):
        request_once(args.url, args.method, headers, args.body, args.timeout)
    results = [request_once(args.url, args.method, headers, args.body, args.timeout) for _ in range(max(1, args.requests))]
    durations = [item["durationMs"] for item in results]
    report = {
        "url": args.url,
        "method": args.method.upper(),
        "requests": len(results),
        "successes": sum(1 for item in results if item["ok"]),
        "failures": sum(1 for item in results if not item["ok"]),
        "durationMs": {
            "min": min(durations),
            "max": max(durations),
            "mean": statistics.mean(durations),
            "median": statistics.median(durations),
            "p95": percentile(durations, 95),
        },
        "statuses": {},
        "errors": [item["error"] for item in results if item["error"]][:10],
    }
    for item in results:
        key = str(item["status"])
        report["statuses"][key] = report["statuses"].get(key, 0) + 1
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
