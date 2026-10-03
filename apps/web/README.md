# web

The personal website: a Next.js app using Clerk for auth.

## Run locally

```sh
pnpm install
pnpm --filter web dev
```

## Checks

Forgejo CI (`.forgejo/workflows/ci.yml`) runs, from the repo root:

```sh
pnpm exec biome check apps/web
pnpm --filter web typecheck
pnpm --filter web build
```

`build` needs the `NEXT_PUBLIC_*` env vars (Clerk publishable key, Umami
website ID, domain, redirect URL) — see `ci.yml` for the placeholder values
CI uses.

## Deploys

Deploys run from the GitHub mirror (`.github/workflows/personal-website.yaml`
via Vercel), not from Forgejo.
