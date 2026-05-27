# Implementation Patterns

Use this file during the Develop phase when deciding how to build the frontend.

## Existing Projects

Follow local conventions first.

- Reuse existing layout shells, route wrappers, providers, and component primitives.
- Match existing naming, folder structure, import aliases, and styling conventions.
- Use the installed icon library instead of adding hand-written SVGs for common actions.
- Keep data fetching and mutation patterns aligned with the app's current client/server boundary.
- Keep state local unless multiple routes or distant components need to share it.
- Prefer existing form, table, modal, toast, tooltip, and menu patterns.
- Add tests in the style already present in the repo.

Avoid introducing:

- A new component library for one screen
- A new state manager for local interaction state
- A new CSS framework where the app already has one
- Global CSS changes for a local component unless tokens or resets are actually needed

## Greenfield Defaults

Pick the simplest stack that satisfies the request.

- Use plain HTML/CSS/JS for small static pages, simple prototypes, and single-file artifacts.
- Use React + TypeScript + Vite for interactive single-page apps when no stack is specified.
- Use Next.js only when routing, server rendering, file-based routes, or backend integration is part of the request.
- Use Tailwind only when the project already uses it or rapid component styling is valuable.
- Use shadcn/ui only for component-rich apps where its primitives reduce real implementation work.

## Component Design

Build semantic structure before visual polish.

- Use headings in logical order.
- Use `main`, `nav`, `section`, `aside`, `form`, `table`, `button`, and `a` appropriately.
- Use buttons for commands and links for navigation.
- Keep components cohesive: split when a subpart has its own state, behavior, reuse, or complexity.
- Do not split purely to create many files.

For fixed-format UI such as grids, dashboards, boards, control bars, metric cards, and tool palettes:

- Use stable dimensions.
- Set predictable min/max widths.
- Ensure labels and dynamic values do not resize the whole layout.
- Ensure hover and focus states do not shift neighboring elements.

## Visual Quality

Choose a visual direction that fits the domain.

- Operational tools should feel dense, clear, and work-focused.
- Consumer apps can be more expressive.
- Editorial or portfolio pages can use larger type and stronger art direction.
- Games and creative tools can be more animated and playful.

Avoid common weak defaults:

- Purple-blue gradients as the main visual idea
- Oversized centered hero sections for tools and dashboards
- Decorative cards around every section
- Cards nested inside cards
- Orbs, bokeh blobs, and generic abstract decorations
- One-note palettes where every surface is a tint of the same hue
- Text that scales directly with viewport width

Use:

- Clear hierarchy
- Intentional typography
- Consistent spacing
- Strong contrast
- Real icons for common tools
- Meaningful empty, loading, error, disabled, hover, focus, and active states

## Responsive Behavior

Define breakpoints by content, not by arbitrary device names.

- Verify narrow mobile, standard desktop, and any layout-specific breakpoint.
- Avoid horizontal scrolling on mobile unless the interface is intentionally a data grid.
- Wrap long controls or move secondary actions into menus.
- Keep tap targets comfortably sized.
- Ensure sticky headers, sidebars, and bottom bars do not cover content.

## Accessibility Baseline

Include:

- Programmatic labels for inputs and icon-only buttons
- Visible focus states
- Keyboard access for core interactions
- Dialog focus management when dialogs are used
- Sufficient color contrast
- Reduced-motion handling for large animations where appropriate
- Alt text for meaningful images and empty alt for decorative images

## Mock Data

If mock data is needed:

- Keep it isolated in a fixture, local constant, or mock module.
- Make it realistic enough to exercise long labels, empty values, and edge cases.
- Do not hardcode throwaway examples throughout component markup.
- Mention in the final response when mock data was added.
