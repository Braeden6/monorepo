FROM node:23-alpine AS base

FROM base AS builder
RUN apk add --no-cache libc6-compat
WORKDIR /app
RUN npm install -g turbo
COPY . .
RUN turbo prune recipe --docker

FROM base AS installer
RUN apk add --no-cache libc6-compat
WORKDIR /app
RUN npm install -g pnpm

COPY --from=builder /app/out/json/ .
COPY --from=builder /app/out/pnpm-lock.yaml ./pnpm-lock.yaml
RUN pnpm install --frozen-lockfile --include-workspace-root


COPY --from=builder /app/out/full/ .
COPY turbo.json turbo.json


ENV NEXT_TELEMETRY_DISABLED=1

RUN pnpm turbo run build --filter=recipe...


FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

RUN mkdir .next
RUN chown nextjs:nodejs .next

COPY --from=installer --chown=nextjs:nodejs /app/apps/recipe/.next/standalone ./
COPY --from=installer --chown=nextjs:nodejs /app/apps/recipe/.next/static ./apps/recipe/.next/static
COPY --from=installer --chown=nextjs:nodejs /app/apps/recipe/public ./apps/recipe/public

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "apps/recipe/server.js"]