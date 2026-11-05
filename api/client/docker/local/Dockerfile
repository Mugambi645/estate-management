# syntax=docker/dockerfile:1

FROM docker.io/node:22-alpine AS base

# ---------- Stage 1: install dependencies ----------
FROM base AS node-build-stage

RUN apk add --no-cache libc6-compat

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=cache,target=/usr/local/share/.cache/yarn \
    --mount=type=cache,target=/root/.local/share/pnpm/store \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
    else echo "Lockfile not found." && exit 1; \
    fi

# ---------- Stage 2: runtime ----------
FROM base AS node-run-stage

RUN apk add --no-cache libc6-compat

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

# Installed deps from the build stage
COPY --from=node-build-stage /app/node_modules ./node_modules

# App source (client/.dockerignore keeps host node_modules/.next out of this)
COPY . ${APP_HOME}

# Pre-create .next so the named volume mounted there is owned by `node`
RUN mkdir -p ${APP_HOME}/.next \
    && chown -R node:node ${APP_HOME}

USER node

EXPOSE 3000

# Safety net: if the node_modules volume is stale and missing the Tailwind
# PostCSS plugin, install before starting the dev server.
CMD ["sh", "-c", "[ -d node_modules/@tailwindcss/postcss ] || npm install; npm run dev"]