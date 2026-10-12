# apps/web

The personal website: a Next.js app using Clerk for auth.

## Run locally

```sh
pnpm install
pnpm --filter web dev
```

## Checks (Forgejo CI: `.forgejo/workflows/ci.yml`)

From the repo root:

```sh
pnpm exec biome check apps/web   # root biome, not `pnpm --filter web lint`
pnpm --filter web typecheck
pnpm --filter web build
```

`build` needs the `NEXT_PUBLIC_*` env vars (Clerk key, Umami ID, domain,
redirect URL) at build time; see `ci.yml` for the placeholder values CI uses.

## Deploys

Deploys come from the GitHub mirror (`.github/workflows/personal-website.yaml`
via Vercel), not from Forgejo CI.
