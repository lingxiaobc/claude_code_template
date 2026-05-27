#!/usr/bin/env python3
"""Generic browser health check for frontend work.

This script opens a URL with Playwright, records console and network failures,
captures desktop and mobile screenshots, and runs lightweight DOM checks for
common frontend regressions.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_VIEWPORTS = {
    "desktop": {"width": 1440, "height": 1000},
    "mobile": {"width": 375, "height": 812},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a frontend route with browser screenshots, console checks, and DOM health checks."
    )
    parser.add_argument("url", help="URL to verify, for example http://localhost:5173/dashboard")
    parser.add_argument(
        "--out-dir",
        default="frontend-verification",
        help="Directory for screenshots and report.json. Default: frontend-verification",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30000,
        help="Navigation timeout in milliseconds. Default: 30000",
    )
    parser.add_argument(
        "--wait",
        default="networkidle",
        choices=["load", "domcontentloaded", "networkidle"],
        help="Load state to wait for. Default: networkidle",
    )
    parser.add_argument(
        "--viewport",
        action="append",
        default=[],
        metavar="NAME:WIDTHxHEIGHT",
        help="Extra viewport to check, for example tablet:768x1024. Can be repeated.",
    )
    parser.add_argument(
        "--full-page",
        action="store_true",
        help="Capture full-page screenshots instead of viewport screenshots.",
    )
    return parser.parse_args()


def parse_viewports(values: list[str]) -> dict[str, dict[str, int]]:
    viewports = dict(DEFAULT_VIEWPORTS)
    for raw in values:
        try:
            name, size = raw.split(":", 1)
            width, height = size.lower().split("x", 1)
            viewports[name] = {"width": int(width), "height": int(height)}
        except ValueError as exc:
            raise SystemExit(f"Invalid --viewport value: {raw!r}. Expected NAME:WIDTHxHEIGHT.") from exc
    return viewports


def run_dom_checks(page: Any) -> dict[str, Any]:
    return page.evaluate(
        """
        () => {
          const result = {
            title: document.title || "",
            bodyTextLength: (document.body && document.body.innerText || "").trim().length,
            documentWidth: document.documentElement.scrollWidth,
            viewportWidth: window.innerWidth,
            horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
            clippedElements: [],
            unnamedButtons: [],
            imagesMissingAlt: [],
            fixedElements: [],
          };

          const isVisible = (el) => {
            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();
            return style.display !== "none" &&
              style.visibility !== "hidden" &&
              rect.width > 0 &&
              rect.height > 0;
          };

          for (const el of Array.from(document.querySelectorAll("body *"))) {
            if (!isVisible(el)) continue;
            const style = window.getComputedStyle(el);
            const tag = el.tagName.toLowerCase();

            if (
              result.clippedElements.length < 25 &&
              (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) &&
              ["hidden", "clip", "auto", "scroll"].includes(style.overflow)
            ) {
              const text = (el.innerText || el.getAttribute("aria-label") || "").trim().slice(0, 80);
              result.clippedElements.push({
                tag,
                className: String(el.className || "").slice(0, 120),
                id: el.id || "",
                text,
                clientWidth: el.clientWidth,
                scrollWidth: el.scrollWidth,
                clientHeight: el.clientHeight,
                scrollHeight: el.scrollHeight,
              });
            }

            if (result.fixedElements.length < 20 && ["fixed", "sticky"].includes(style.position)) {
              const rect = el.getBoundingClientRect();
              result.fixedElements.push({
                tag,
                className: String(el.className || "").slice(0, 120),
                id: el.id || "",
                position: style.position,
                rect: {
                  x: Math.round(rect.x),
                  y: Math.round(rect.y),
                  width: Math.round(rect.width),
                  height: Math.round(rect.height),
                },
              });
            }
          }

          for (const button of Array.from(document.querySelectorAll("button, [role='button']"))) {
            if (!isVisible(button)) continue;
            const name = (
              button.innerText ||
              button.getAttribute("aria-label") ||
              button.getAttribute("title") ||
              ""
            ).trim();
            if (!name && result.unnamedButtons.length < 25) {
              result.unnamedButtons.push({
                tag: button.tagName.toLowerCase(),
                className: String(button.className || "").slice(0, 120),
                id: button.id || "",
              });
            }
          }

          for (const img of Array.from(document.images)) {
            if (!isVisible(img)) continue;
            if (!img.hasAttribute("alt") && result.imagesMissingAlt.length < 25) {
              result.imagesMissingAlt.push({
                src: img.currentSrc || img.src || "",
                className: String(img.className || "").slice(0, 120),
                id: img.id || "",
              });
            }
          }

          return result;
        }
        """
    )


def main() -> int:
    args = parse_args()
    viewports = parse_viewports(args.viewport)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Playwright is not installed. Install it with `pip install playwright` and `python -m playwright install chromium`.",
            file=sys.stderr,
        )
        return 2

    report: dict[str, Any] = {
        "url": args.url,
        "viewports": {},
        "console": [],
        "failedRequests": [],
        "errors": [],
        "status": "success",
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def on_console(msg: Any) -> None:
            if msg.type in {"error", "warning"}:
                report["console"].append({"type": msg.type, "text": msg.text})

        def on_request_failed(request: Any) -> None:
            failure = request.failure
            report["failedRequests"].append(
                {
                    "url": request.url,
                    "method": request.method,
                    "errorText": failure.get("errorText") if failure else "unknown",
                }
            )

        page.on("console", on_console)
        page.on("requestfailed", on_request_failed)

        for name, viewport in viewports.items():
            page.set_viewport_size(viewport)
            viewport_report: dict[str, Any] = {"viewport": viewport}
            try:
                response = page.goto(args.url, wait_until=args.wait, timeout=args.timeout)
                viewport_report["httpStatus"] = response.status if response else None
                screenshot_path = out_dir / f"{name}.png"
                page.screenshot(path=str(screenshot_path), full_page=args.full_page)
                viewport_report["screenshot"] = str(screenshot_path)
                viewport_report["dom"] = run_dom_checks(page)
            except PlaywrightError as exc:
                viewport_report["error"] = str(exc)
                report["errors"].append({"viewport": name, "error": str(exc)})
            report["viewports"][name] = viewport_report

        browser.close()

    issue_count = (
        len(report["console"])
        + len(report["failedRequests"])
        + len(report["errors"])
        + sum(
            1
            for viewport in report["viewports"].values()
            if viewport.get("dom", {}).get("horizontalOverflow")
            or viewport.get("dom", {}).get("clippedElements")
            or viewport.get("dom", {}).get("unnamedButtons")
            or viewport.get("dom", {}).get("imagesMissingAlt")
        )
    )
    if issue_count:
        report["status"] = "issues_found"

    report_path = out_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(report_path)}, indent=2))
    return 1 if report["status"] == "issues_found" else 0


if __name__ == "__main__":
    raise SystemExit(main())
