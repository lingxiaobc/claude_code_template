---
name: frontend-development-workflow
description: "End-to-end frontend development workflow for building or modifying web apps, pages, components, dashboards, HTML/CSS/JS interfaces, React/Vue/Svelte projects, or UI artifacts. Use when the user asks to create, redesign, implement, fix, or polish frontend work and expects the model to plan first, orchestrate the implementation, develop the code, then verify it in a browser. Trigger for requests about frontend development, page development, component development, dashboards, web applications, UI implementation, responsive styling, or visual polish. Do NOT use when the user only asks for backend/API/database work, a design critique with no code changes, or a high-level explanation with no implementation."
---

# Frontend Development Workflow

Use this skill to complete frontend work through four phases:

1. Plan
2. Orchestrate
3. Develop
4. Verify

For new apps, pages, dashboards, redesigns, components, and non-trivial UI fixes, follow the full workflow. For tiny edits, keep the plan brief but still inspect the existing code and verify the affected UI.

## Resource Guide

Load these files only when needed:

- `references/planning-checklist.md`: Use during Plan and Orchestrate for project recon, scope control, and implementation sequencing.
- `references/implementation-patterns.md`: Use during Develop for component structure, styling choices, responsive behavior, accessibility, and mock data handling.
- `references/verification-checklist.md`: Use during Verify for static checks, browser checks, visual QA, responsive QA, and completion criteria.
- `scripts/verify_frontend.py`: Use as a black-box generic browser health check for local frontend routes. Run `python scripts/verify_frontend.py --help` before using it.

## Phase 1: Plan

Inspect the existing project before making architectural or styling decisions.

Read enough context to identify:

- Framework, router, package manager, and dev server command
- Target route, page, component, or artifact
- Styling system, design tokens, component library, and icon library
- Existing UI conventions and test commands
- Primary user, user task, required states, and responsive needs

For substantial work, read `references/planning-checklist.md`.

Ask the user only when a missing decision would cause meaningful rework. Otherwise make a conservative assumption, proceed, and mention the assumption in the final response.

## Phase 2: Orchestrate

Convert the plan into a short implementation sequence before editing code.

Prefer:

- Existing components and local patterns
- Existing routing and state management
- Existing styling conventions
- Focused files and scoped changes
- The smallest architecture that satisfies the request

For greenfield work, choose a simple stack that matches the request. Use plain HTML/CSS/JS for small standalone pages. Use React + TypeScript + Vite for interactive single-page apps unless the user or repo indicates otherwise.

For detailed orchestration guidance, read `references/planning-checklist.md`.

## Phase 3: Develop

Build the actual usable interface, not a placeholder or marketing explanation.

During implementation:

- Use semantic structure before visual polish.
- Match the repo's component, styling, import, and naming patterns.
- Include real expected states: loading, empty, error, disabled, success, hover, focus, and active where relevant.
- Use stable responsive constraints so labels, counts, loading text, and hover states do not shift the layout.
- Use icons for familiar actions when an icon library exists.
- Avoid unrelated refactors.

Avoid generic AI-looking UI:

- Default purple gradients
- Decorative blobs or orbs
- Unnecessary card-heavy page sections
- Cards nested inside cards
- Oversized centered hero layouts for dashboards or tools
- One-note palettes unless required by brand

For detailed implementation guidance, read `references/implementation-patterns.md`.

## Phase 4: Verify

Do not finish after coding. Verify the frontend unless the environment cannot run it.

Run available static checks from the repo:

- Type check
- Lint
- Unit or component tests
- Build
- Existing browser tests

Then run browser verification when the app can launch locally:

1. Start the dev server with the repo's script.
2. Open the relevant route.
3. Wait for the app to render.
4. Check console errors and failed requests.
5. Check desktop and mobile layouts.
6. Exercise the primary interaction.
7. Fix issues and re-run affected checks.

For a generic page health check, use:

```bash
python scripts/verify_frontend.py --help
python scripts/verify_frontend.py http://localhost:5173
```

For task-specific interactions, write focused Playwright automation instead of relying only on the generic script.

For detailed QA guidance, read `references/verification-checklist.md`.

## Final Response

When complete, report:

- What changed
- Key files touched
- Static checks run
- Browser checks run
- Any verification that could not run and why
- The local URL if a dev server is running for user inspection

Keep the final response concise and factual.
