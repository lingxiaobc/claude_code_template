# Rewrite Workflow

Use this for rewrites and substantial refactors.

## Principle

Do not change behavior and structure at the same time unless the user explicitly asks for a behavior change. Lock behavior first, then rewrite.

## Before Rewriting

Identify:

- Public API or module contract
- Existing tests
- Important edge cases
- Error behavior
- Data side effects
- Performance expectations
- Rollback path

If tests are missing, add characterization tests for the current behavior before large changes.

## Rewrite Strategy

Prefer small steps:

1. Add or update tests that describe current behavior.
2. Extract boundaries if needed.
3. Replace internals behind the same interface.
4. Run tests after each meaningful step.
5. Remove dead code only after replacement is verified.

Avoid:

- Big-bang rewrites
- Renaming and behavior changes in the same patch
- New dependencies without need
- Changing response shape during internal refactor
- Removing fallback paths before verification

## Equivalence Checks

Verify:

- Same inputs produce same expected outputs
- Same errors occur for invalid inputs
- Same auth and permission behavior remains
- Same database side effects remain
- Same public types or schemas remain unless intentionally changed

## When To Stop And Ask

Ask the user when the rewrite uncovers:

- Ambiguous old behavior
- Missing business rule
- Data migration need
- Breaking public contract
- Security behavior not covered by code
