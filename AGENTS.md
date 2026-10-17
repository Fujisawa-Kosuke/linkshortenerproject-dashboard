# AGENTS.md

Guidance for AI coding agents (GitHub Copilot, Copilot CLI, and others) working in this
repository. Read this file first. Deep-dive topic docs live in [`docs/`](./docs) and
[`.github/instructions/`](./.github/instructions) — follow the links below rather than
guessing at conventions.

For detailed guidelines on specific topics, refer to the modular documentation in the '/docs' directory. ALWAYS refer to the relevant .md file BEFORE generating any code:

## Project Overview

A link-shortener dashboard application. Signed-in users create, edit, and delete
shortened links; visiting `/l/{shortCode}` redirects to the original URL. Built as part
of a GitHub Copilot training course.

## Tech Stack (summary)

Next.js 16 (App Router) + React 19 + TypeScript (strict) + Tailwind CSS v4 + shadcn/ui +
Clerk (auth) + Drizzle ORM + Neon Postgres + Zod. Full details, versions, and the
auto-formatting hook: [`docs/tech-stack.md`](./docs/tech-stack.md).

## Repository Map

```text
app/            Routes: landing page, protected /dashboard, public /l/[shortcode] redirect
components/ui/  shadcn/ui primitives only — install via the shadcn CLI, don't hand-roll
data/           The ONLY place Drizzle queries are written (data access layer)
db/             Drizzle client + schema (db/schema.ts)
drizzle/        Generated SQL migrations — never hand-edit
lib/            Shared utilities (cn() class helper)
docs/           Deep-dive reference docs (see docs/README.md)
.github/instructions/  Auto-attached, topic-specific Copilot instructions
.agents/skills/         Project skills (e.g. monthly-links-chart)
```

Full breakdown and "where does new code go" guidance:
[`docs/project-structure.md`](./docs/project-structure.md).

## Setup & Commands

```bash
npm install        # install dependencies
npm run dev        # start the dev server
npm run build      # production build
npm run lint       # ESLint — run before finishing any change
npx drizzle-kit generate   # generate a migration after editing db/schema.ts
npx drizzle-kit migrate    # apply pending migrations
```

Required environment variables (`DATABASE_URL`, Clerk keys) are documented in
[`docs/environment-variables.md`](./docs/environment-variables.md). There is currently no
automated test suite in this repository — validate changes with `npm run lint` and
`npm run build`, and by reasoning through the affected flows manually.

## Must-Follow Conventions

These are non-negotiable, enforced project-wide. Each links to the full instructions:

1. **Authentication is Clerk-only.** No custom auth, no alternative libraries, sign-in/up
   must be modal-based. → [`.github/instructions/authentication.instructions.md`](./.github/instructions/authentication.instructions.md)
2. **Data fetching happens in Server Components, via `/data` helpers.** Never fetch data
   in a Client Component; never query Drizzle outside `/data`. → [`.github/instructions/data-fetching.instructions.md`](./.github/instructions/data-fetching.instructions.md)
3. **Mutations are Server Actions in a colocated `actions.ts`.** Must validate input with
   Zod, check `auth()`, call `/data` helpers (never raw Drizzle), and return
   `{ success | error }` instead of throwing. → [`.github/instructions/server-actions.instructions.md`](./.github/instructions/server-actions.instructions.md)
4. **UI is built exclusively with shadcn/ui.** Don't hand-write components that shadcn
   already provides. → [`.github/instructions/ui-components.instructions.md`](./.github/instructions/ui-components.instructions.md)
5. **Always verify resource ownership** (`userId` from Clerk) before reading/mutating a
   user's rows — see the pattern in `data/links.ts`.
6. **Validate any stored/user-supplied URL before redirecting to it** (scheme allow-list
   of `http:`/`https:` only) — see [`docs/link-redirection.md`](./docs/link-redirection.md).

## Coding Style Quick Reference

TypeScript strict mode, `@/*` import alias, kebab-case filenames, PascalCase components,
named exports, dev-only error logging, Tailwind + `cn()` for styling. Formatting runs
automatically after edits via a post-tool-use hook (Prettier). Full details:
[`docs/coding-conventions.md`](./docs/coding-conventions.md).

## Documentation Index

See [`docs/README.md`](./docs/README.md) for the same index with more context.

## Available Skills

- `monthly-links-chart` — generates a bar chart of links created per month from the
  database (see `.agents/skills/monthly-links-chart`).
- `skill-creator` — guide for authoring new skills.

## Before Finishing a Change

- Run `npm run lint` and fix any new warnings/errors.
- Run `npm run build` for changes that could affect routing, types, or the build.
- Re-read the relevant instructions file(s) above if the change touches auth, data
  fetching, server actions, UI components, or the redirect route.
