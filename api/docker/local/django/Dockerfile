FROM docker.io/python:3.13-slim-bookworm AS python

# ---------- Stage 1: build wheels with uv ----------
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Install uv (pinned via the official image copy — fastest/safest method)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy just the dependency manifests first for better layer caching
COPY pyproject.toml uv.lock ./

# Build wheels from the lockfile into /wheels
RUN uv export --frozen --no-emit-project --no-dev \
      $( [ "$BUILD_ENVIRONMENT" = "local" ] && echo "" || echo "--no-dev" ) \
      -o /tmp/requirements.txt || true

# Simpler + more robust: build wheels directly from the lockfile
RUN uv build --wheel --out-dir /tmp/dist 2>/dev/null || true

RUN mkdir -p /wheels && \
    uv export --frozen --no-emit-project \
        $( [ "$BUILD_ENVIRONMENT" = "local" ] && echo "--all-groups" || echo "--no-dev" ) \
        --format requirements-txt -o /tmp/requirements.txt && \
    pip wheel --wheel-dir /wheels -r /tmp/requirements.txt

# ---------- Stage 2: runtime ----------
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT} \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o \
       APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles

# Install from the wheels built in stage 1 — no network access needed
COPY --from=python-build-stage /wheels /wheels/
RUN uv pip install --system --no-index --find-links=/wheels/ /wheels/*.whl \
    && rm -rf /wheels/

COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY --chown=django:django ./docker/local/django/start.sh /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

COPY --chown=django:django . ${APP_HOME}
RUN chown django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]