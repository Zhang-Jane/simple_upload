FROM python:3.10-slim as base

# Create a non-root user to run the app with.
RUN groupadd --gid 1000 user &&  adduser --disabled-password --gecos '' --uid 1000 --gid 1000 user
USER user

WORKDIR /home/user/app

# Install Poetry.
RUN --mount=type=cache,target=/root/.cache pip install --user poetry==1.4.2
ENV \
    PATH="/home/user/.local/bin:/home/user/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

COPY --chown=user:user ./pyproject.toml ./poetry.lock ./alembic.ini ./
RUN --mount=type=cache,target=/root/.cache poetry install

FROM base as dev

COPY --chown=user:user ./api api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]


FROM base as test

USER root
RUN apt-get update && apt-get install -y --no-install-recommends git-core
USER user

RUN --mount=type=cache,target=/root/.cache poetry install --with dev

# For running pre-commit
COPY --chown=user:user ./.git .git
COPY --chown=user:user ./.pre-commit-config.yaml .pre-commit-config.yaml

RUN mkdir /home/user/.mypy_cache && chown -R user:user /home/user/.mypy_cache
RUN pre-commit install --install-hooks

COPY --chown=user:user ./api api

# Default target.
FROM dev
