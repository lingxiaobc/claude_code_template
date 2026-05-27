# Planning Checklist

Use this file during the Plan and Orchestrate phases for non-trivial frontend work.

## Project Recon

Read enough code to answer:

- Which framework owns the UI: React, Next.js, Vue, Svelte, Astro, plain HTML, or another stack?
- How is routing handled?
- Where are reusable components stored?
- Where are layout shells, nav, providers, and global styles defined?
- Which styling system is used: Tailwind, CSS modules, Sass, vanilla CSS, CSS-in-JS, component library tokens, or custom tokens?
- Which icon library is already installed?
- Which commands exist for dev, build, lint, typecheck, unit tests, and browser tests?
- Is there an existing Playwright, Cypress, Storybook, or visual testing setup?

Prefer these sources:

- `package.json`
- framework config files
- app route or page directories
- component directories
- global CSS/theme/token files
- existing tests near the target surface

## User and Experience

Identify:

- Primary user
- Primary job the interface must support
- First screen or route the user will see
- Critical user path
- Required inputs, outputs, and state changes
- Required empty, loading, error, disabled, and success states
- Data source or mock data boundary
- Responsive needs: mobile-first, desktop-first, dashboard desktop, kiosk, embedded widget, etc.
- Accessibility needs: keyboard flow, labels, focus management, contrast, reduced motion

If the user did not specify details, infer conservative defaults from the product type and existing app.

## Scope Control

Before editing, decide:

- Which files must change?
- Which existing components can be reused?
- Which new components are justified?
- Which behavior can be mocked for this task?
- Which behavior must be real?
- Which checks prove the work is done?

Avoid:

- Broad refactors unrelated to the requested UI
- Introducing a new design system into an existing app
- Replacing routing or state management to solve a local UI task
- Building a landing page when the user asked for an app or tool

## Plan Shape

For substantial work, keep an internal checklist:

1. Identify target files and route.
2. Confirm layout and component structure.
3. Implement data/state and interactions.
4. Implement responsive behavior.
5. Add accessibility and edge states.
6. Run static checks.
7. Run browser verification.
8. Fix issues and repeat affected checks.

Expose the plan to the user only when the work is large, risky, or the user asked for it.
