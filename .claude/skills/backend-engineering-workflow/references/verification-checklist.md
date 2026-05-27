# Verification Checklist

Use this before final response.

## Static Checks

Run project-native commands when available:

- Typecheck or compile
- Lint
- Format check
- Unit tests
- Integration tests
- Build
- Schema generation

## HTTP Checks

When a server can run:

1. Start it with the repo's script.
2. Check at least one happy path.
3. Check at least one error path.
4. Check auth or forbidden behavior when relevant.
5. Confirm write side effects when practical.

Use `scripts/verify_api.py` for generic HTTP checks.

## Risk Scan

For backend changes with auth, data, SQL, files, or external calls, run or consider `scripts/scan_backend_risks.py`. Treat findings as review prompts, not definitive proof.

## Optimization Verification

For optimization tasks:

- Capture before/after timing when possible.
- Confirm behavior did not change.
- Confirm relevant tests pass.
- Report measurement limits.

## Rewrite Verification

For rewrites:

- Run characterization tests.
- Run existing tests for the module.
- Confirm public contract remains stable.
- Report intentional behavior changes.

## Completion Criteria

Do not declare success until:

- The requested behavior is implemented.
- Relevant checks ran or limitations are reported.
- API behavior was verified when applicable.
- Security/auth behavior was checked when relevant.
- Remaining uncertainty is stated.
