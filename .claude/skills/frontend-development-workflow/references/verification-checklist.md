# Verification Checklist

Use this file during the Verify phase.

## Static Checks

Prefer repo scripts. Inspect `package.json` and use the commands already available.

Common checks:

- Type check
- Lint
- Unit tests
- Component tests
- End-to-end tests
- Production build

Do not invent a new toolchain if the repo already has one.

If dependencies are missing or commands fail for environment reasons, continue with checks that are still possible and report the limitation.

## Browser Checks

When the app can run locally:

1. Start the dev server with the repo's existing script.
2. Open the relevant route.
3. Wait for the app to finish rendering.
4. Check browser console errors.
5. Check failed network requests.
6. Capture desktop and mobile screenshots.
7. Exercise the primary user path.
8. Inspect layout at narrow and desktop widths.
9. Fix issues and re-run affected checks.

Use `scripts/verify_frontend.py` when a generic page health check is enough. Use custom Playwright automation when the core interaction path needs task-specific clicks, typing, or assertions.

## Generic Visual QA

Assume the first render has problems. Look for:

- Text clipped inside buttons, cards, inputs, nav items, charts, tables, or badges
- Headings wrapping into controls or decorative lines
- Low contrast text or icons
- Disabled elements that look active
- Interactive elements without hover or focus states
- Layout shift when counts, labels, or loading text changes
- Repeated items with inconsistent spacing
- Cards or panels too close to each other
- Elements too close to viewport edges
- Modal, popover, dropdown, or tooltip clipping
- Sticky headers, sidebars, or bottom bars covering content
- Accidental horizontal scroll on mobile
- Empty states missing for empty data
- Loading states that leave a blank page
- Error states that are not recoverable
- Placeholder copy left in the UI

## Responsive QA

Check at minimum:

- Narrow mobile: about 375px wide
- Standard desktop: about 1440px wide

Also check any breakpoint where the layout changes.

Verify:

- Navigation remains usable
- Primary actions stay visible
- Text wraps cleanly
- Tables, charts, and grids remain readable
- Touch targets are large enough
- No horizontal scroll unless intentional
- Media is not cropped in a way that hides important content

## Interaction QA

Exercise the primary path:

- Click primary and secondary actions
- Submit forms with valid and invalid input
- Navigate between tabs or views
- Open and close menus, dialogs, popovers, and drawers
- Confirm keyboard access for critical controls
- Confirm loading, success, and error feedback

## Console and Network QA

Treat these as issues unless clearly expected:

- JavaScript exceptions
- React hydration errors
- Failed static asset loads
- Failed API requests
- CORS errors
- Source map errors that obscure real failures

## Completion Bar

Do not declare success until:

- The target route renders.
- The main interaction works.
- Desktop and mobile layouts have been checked.
- Console errors have been reviewed.
- Any static checks that can run have run.
- Known limitations are reported.
