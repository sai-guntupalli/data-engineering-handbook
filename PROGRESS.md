# Progress

## Current Status

Master-based feature branch `feat/handbook-mockups` adds three static, modern SaaS-style HTML mockups under `docs/mockups/`; awaiting review.

## Completed

- [x] 2026-11-07 — Created `feat/handbook-mockups` from `master` in an isolated worktree.
- [x] 2026-11-07 — Shared design system `docs/mockups/styles.css` (tokens on `:root`, light and dark, responsive at 900px and 560px).
- [x] 2026-11-07 — Screen 01 `docs/mockups/01-library.html`: stats, topic filters, grouped notebook cards, starring.
- [x] 2026-11-07 — Screen 02 `docs/mockups/02-notebook.html`: notebook reader with code cells, callouts, sticky table of contents, pager.
- [x] 2026-11-07 — Screen 03 `docs/mockups/03-search.html`: ⌘K command palette with grouped results and keyboard hints.
- [x] 2026-11-07 — Index page `docs/mockups/index.html` with screen links and colour tokens.
- [x] 2026-11-07 — README section describing how to open the mockups.

## In Progress

- Nothing. Waiting for design review of the mockups.

## Next Steps

1. Review the three screens in `docs/mockups/` on desktop, tablet and phone widths; note any visual changes wanted.
2. If approved, port the tokens in `docs/mockups/styles.css` into `app/globals.css` and rebuild `app/page.tsx` and `components/NotebookCard.tsx` to match screen 01.
3. Port screen 02 into the notebook view and screen 03 into the search page (`app/search`), keeping the existing data from `lib/notebooks.ts`.
4. Add interaction behaviour to the palette (`⌘K` opens, arrow keys move the selection, `Enter` opens) in the real app, not in the mockup.

## Blockers

- None.
