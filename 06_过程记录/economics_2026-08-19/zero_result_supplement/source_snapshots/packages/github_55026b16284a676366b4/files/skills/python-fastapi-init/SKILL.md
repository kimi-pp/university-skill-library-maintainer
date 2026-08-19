---
name: python-fastapi-init
description: Bootstrap a new FastAPI service with uv + the canonical strict baseline — Ruff with curated extend-select, mypy strict with extra error codes, pytest baseline. Installs the latest FastAPI, sets up a Pydantic Settings module with sensible API defaults, scaffolds a `/healthz` endpoint with its smoke test. Asks the user the Python version and whether to use SQLModel, SQLAlchemy 2.x, or no ORM. **Deliberately skips database driver installation** — pick yours and add it once the connection string is set. Use whenever the user asks to "create / initialize / scaffold / bootstrap / start" a FastAPI project, service, API, or backend.
---

# FastAPI service initialization

Apply this skill end-to-end whenever bootstrapping a new HTTP service with FastAPI. The configs below are designed to work together. Deviations need to be justified in the PR that introduces them.

What this skill does:
- Scaffolds a uv-managed package with src-layout.
- Pins the strict Ruff / mypy / pytest baseline tied to the chosen Python version.
- Installs the **latest** FastAPI release (no version cap — `uv` resolves on the fly).
- Wires a Pydantic Settings module with the env vars every API needs.
- Creates a runnable app with CORS middleware + `/healthz` + its smoke test.
- Optionally adds `sqlmodel` or `sqlalchemy[asyncio]` + `alembic`. **No database driver is installed** — the user picks `asyncpg`, `psycopg`, `aiosqlite`, etc. once they know where the DB lives.

What this skill explicitly does NOT do:
- Install any database driver (`asyncpg`, `psycopg`, `aiomysql`, `aiosqlite`, …).
- Wire authentication. Pick your own (OAuth2 with passlib + python-jose, NextAuth on the frontend with a JWT verifier, API keys via dependency, …).
- Scaffold Alembic. Mentioned in the cheat sheet; running `alembic init` is left to the user once they've picked a driver.
- Containerise. A Dockerfile is per-project; it depends on the deploy target.

## Before you start

Verify with **Bash** that the user has the right tooling. **Always check current versions first** — pinned numbers below were correct when this skill was written and drift over time. Use newer if available; do not downgrade.

```bash
# uv — bumps almost monthly
uv --version

# git and (recommended) gh
git --version && gh --version
```

If `uv` is missing:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Step 1 — Ask the user

Three questions, one prompt:

1. **Project / package name** (e.g. `myapi`, snake_case, no hyphens — becomes the importable name).
2. **Python version**. Quick guide as of writing:

   | Version | Status | Pick when… |
   |---|---|---|
   | **3.14** | Latest stable (Oct 2025) | Default. Faster start-up, better error messages. |
   | **3.13** | Mature stable | A critical dep hasn't published 3.14 wheels yet. |
   | **3.12** | Maintenance | Integrating with an existing 3.12 project. |
   | **≤ 3.11** | EOL or near-EOL | Avoid unless required. |

   Default to **3.14**.

3. **ORM choice**: `sqlmodel`, `sqlalchemy`, or `none`.
   - **`sqlmodel`** — Pydantic + SQLAlchemy in one model class. Less boilerplate for small CRUD APIs; the abstraction can hurt once queries get complex.
   - **`sqlalchemy`** — SQLAlchemy 2.x with `Mapped[...]` syntax. Industrial-strength, ergonomic since 2.0, decouples request/response models from DB rows.
   - **`none`** — No ORM. Skip the `database_url` setting and the SQL-related deps.

Make sure `uv` knows about the chosen Python:
```bash
uv python install <version>
uv python list
```

## Step 2 — Scaffold with `uv init --package`

```bash
uv init --package --python <version> <package-name>
cd <package-name>
```

Layout produced:
```
<package-name>/
├── .python-version
├── pyproject.toml
├── README.md
└── src/
    └── <package_name>/
        └── __init__.py
```

The next step **replaces** `pyproject.toml`.

## Step 3 — Replace `pyproject.toml`

Write **exactly** this, substituting `<package_name>`, `<python-version>` (e.g. `3.14`), and `<py-tag>` (e.g. `py314`):

```toml
[project]
name = "<package_name>"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=<python-version>"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[dependency-groups]
dev = [
    "ruff>=0.7",
    "mypy>=1.13",
    "pytest>=8",
    "pytest-cov>=5",
    "pytest-asyncio>=0.24",
    "pytest-mock>=3.14",
    "pytest-randomly>=3.15",
    "time-machine>=2.15",
    "httpx>=0.27",          # used by fastapi.testclient
    "respx>=0.21",          # mocks outbound httpx calls in tests
]

[tool.ruff]
target-version = "<py-tag>"
line-length = 88

[tool.ruff.lint]
extend-select = [
    "A",     # flake8-builtins
    "ARG",   # flake8-unused-arguments
    "ASYNC", # flake8-async
    "B",     # flake8-bugbear
    "BLE",   # flake8-blind-except
    "C4",    # flake8-comprehensions
    "C90",   # mccabe
    "DTZ",   # flake8-datetimez
    "E",     # pycodestyle errors
    "EM",    # flake8-errmsg
    "FBT",   # flake8-boolean-trap
    "FLY",   # flynt
    "FURB",  # refurb
    "G",     # flake8-logging-format
    "I",     # isort
    "ICN",   # flake8-import-conventions
    "ISC",   # flake8-implicit-str-concat
    "INT",   # flake8-gettext
    "LOG",   # flake8-logging
    "N",     # pep8-naming
    "PERF",  # perflint
    "PGH",   # pygrep-hooks
    "PIE",   # flake8-pie
    "PL",    # pylint
    "PTH",   # flake8-use-pathlib
    "Q",     # flake8-quotes
    "RET",   # flake8-return
    "RSE",   # flake8-raise
    "RUF",   # ruff-specific rules
    "S",     # flake8-bandit
    "SIM",   # flake8-simplify
    "SLF",   # flake8-self
    "SLOT",  # flake8-slots
    "T10",   # flake8-debugger
    "T20",   # flake8-print
    "TC",    # flake8-type-checking
    "TID",   # flake8-tidy-imports
    "TRY",   # tryceratops
    "UP",    # pyupgrade
    "W",     # pycodestyle warnings
    "YTT",   # flake8-2020
]
ignore = [
    "PLR0913", # too many arguments — sometimes unavoidable
    "PLR2004", # magic value comparison — too many false positives
    "TRY003",  # long exception messages — sometimes clearer inline
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",    # `assert` is how pytest works
    "SLF001",  # tests sometimes peek at private state
]

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"

[tool.ruff.lint.isort]
force-single-line = true
lines-between-types = 1
lines-after-imports = 2
known-first-party = ["<package_name>"]

[tool.mypy]
strict = true
python_version = "<python-version>"
namespace_packages = true
show_error_codes = true
enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
plugins = ["pydantic.mypy"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true

[tool.pytest.ini_options]
minversion = "8.0"
addopts = ["-ra", "--strict-markers", "--strict-config"]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "integration: tests that hit real external services (DB, Redis, HTTP)",
    "slow: tests > 1s",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@overload",
]
show_missing = true
skip_covered = true
```

Notes on what changes vs a non-FastAPI baseline:
- `plugins = ["pydantic.mypy"]` plus the `[tool.pydantic-mypy]` block — Pydantic's mypy plugin catches model construction errors at type-check time (e.g. passing a field that doesn't exist). `init_forbid_extra` forces matching the declared schema; `init_typed` enables full type-checking of model `__init__` calls.
- `httpx` + `respx` land in the dev group — `fastapi.testclient.TestClient` is built on httpx, so tests need it.

## Step 4 — Install the FastAPI stack

The user asked for the **latest** FastAPI release. `uv add` resolves to the newest compatible version at install time and pins it in `uv.lock`. No version specifier required in commands below.

```bash
# runtime deps every FastAPI service needs
uv add fastapi "uvicorn[standard]" pydantic-settings
```

If the user picked **`sqlmodel`**:
```bash
uv add sqlmodel alembic
```

If the user picked **`sqlalchemy`**:
```bash
uv add "sqlalchemy[asyncio]" alembic
```

If **`none`**: skip the ORM install entirely.

`uv add` does two things in one go: writes the dep into `[project].dependencies` in `pyproject.toml` AND syncs the venv. After it returns, the imports work.

**Do NOT install a database driver** at this stage. The user has to make a deploy-target decision (PostgreSQL → `asyncpg`; SQLite → `aiosqlite`; MySQL → `aiomysql` or `asyncmy`; SQL Server → `aioodbc`; etc.) before this matters. Once they know, they add it:
```bash
uv add asyncpg    # example for Postgres + SQLAlchemy/SQLModel async
```

## Step 5 — `py.typed` marker

PEP 561: ship an empty `py.typed` next to `__init__.py` so any code importing this package (sibling services, tests in other repos, etc.) gets the type hints instead of `Any`. Free file, no downsides.

```bash
touch src/<package_name>/py.typed
```

## Step 6 — Settings module

Create `src/<package_name>/config.py`:

```python
"""Application settings, loaded from environment variables.

Pydantic Settings validates each variable on startup. Missing or
malformed env aborts the boot with a clear error — better than a
silent runtime failure on the first request.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


Environment = Literal["dev", "test", "staging", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Application settings.

    Every env var the app reads must be declared here. ``extra="ignore"``
    lets the ``.env`` file coexist with vars from other tools
    (docker-compose, CI, …) without raising.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ── Runtime ─────────────────────────────────────────────────────────
    environment: Environment = "dev"
    log_level: LogLevel = "INFO"
    debug: bool = False

    # ── Application ─────────────────────────────────────────────────────
    app_name: str = "<package_name>"
    api_v1_prefix: str = "/api/v1"

    # ── CORS ────────────────────────────────────────────────────────────
    # Comma-separated list of origins allowed by the CORS middleware.
    # Parse with ``allowed_origins_list``; the raw string lives here so
    # docker-compose / shell env can set it as one value.
    allowed_origins: str = "http://localhost:3000"
[[DB_BLOCK]]
    @property
    def allowed_origins_list(self) -> list[str]:
        """Parsed list of CORS-allowed origins."""
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached singleton Settings instance.

    Tests can mutate env vars and call ``get_settings.cache_clear()``
    to force the next call to re-read them.
    """
    return Settings.model_validate({})
```

Replace `[[DB_BLOCK]]` based on the ORM choice from Step 1:

- If **`sqlmodel`** or **`sqlalchemy`** was picked, insert this block (with the blank line above and below):
  ```python

      # ── Database ────────────────────────────────────────────────────────
      # SQLAlchemy URL, e.g.
      #   postgresql+asyncpg://user:pass@host:5432/db
      #   sqlite+aiosqlite:///./dev.db
      # The driver part (after the +) is what you ``uv add`` separately.
      database_url: str = ""
      database_pool_size: int = 10

  ```

- If **`none`** was picked, just delete the `[[DB_BLOCK]]` placeholder line.

## Step 7 — FastAPI app skeleton

Create `src/<package_name>/main.py`:

```python
"""FastAPI application entry point.

Run locally:
    uv run uvicorn <package_name>.main:app --reload

The ``create_app`` factory exists so tests can build isolated instances
with overridden dependencies (``app.dependency_overrides[...]``) instead
of mutating a shared module-level object.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from <package_name>.config import get_settings


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    @app.get("/healthz", tags=["health"])
    async def healthz() -> dict[str, str]:
        """Liveness probe — answers as long as the process is alive.

        Returns 200 with a constant payload. Anything more elaborate
        (e.g. DB ping) belongs in ``/readyz`` to avoid cascading
        restarts during transient outages.
        """
        return {"status": "ok"}

    return app


app = create_app()
```

Substitute `<package_name>` with the real one. FastAPI auto-publishes `/docs` (Swagger UI), `/redoc` (ReDoc), and `/openapi.json` once the app boots.

## Step 8 — Scaffold `tests/`

```bash
mkdir tests
touch tests/__init__.py
```

Write `tests/conftest.py`:

```python
"""Shared test fixtures."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from <package_name>.config import get_settings
from <package_name>.main import create_app


@pytest.fixture
def app() -> Iterator[FastAPI]:
    """Build a fresh app per test so dependency overrides don't leak."""
    get_settings.cache_clear()
    yield create_app()
    get_settings.cache_clear()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """``TestClient`` wired to the per-test app."""
    return TestClient(app)
```

Write `tests/test_health.py`:

```python
"""Smoke tests — keep them passing through any refactor."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_healthz_returns_ok(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_schema_is_published(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["openapi"].startswith("3.")
```

Substitute `<package_name>` in `conftest.py`.

## Step 9 — `.env` and `.env.example`

`uv init` already added `.env` to `.gitignore` (verify with `cat .gitignore`). Create a committed `.env.example` that documents every variable a deployer needs to set:

```bash
# .env.example — copy to .env and fill in for local dev.
# Every variable here maps to a field on Settings (src/<package_name>/config.py).

# Runtime
ENVIRONMENT=dev
LOG_LEVEL=INFO
DEBUG=false

# Application
APP_NAME=<package_name>
API_V1_PREFIX=/api/v1

# CORS — comma-separated origins
ALLOWED_ORIGINS=http://localhost:3000
```

If the ORM choice was not `none`, append:
```bash
# Database — driver part (postgresql+asyncpg, sqlite+aiosqlite, …) must
# match the driver added with `uv add` separately.
DATABASE_URL=
DATABASE_POOL_SIZE=10
```

Now copy it to `.env` so local development works out of the box:
```bash
cp .env.example .env
```

`.env` stays out of git; `.env.example` is committed and acts as the spec.

## Step 10 — VS Code settings

Write `.vscode/settings.json` (commit it):

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },
  "python.formatting.provider": "none",
  "ruff.importStrategy": "fromEnvironment",
  "mypy-type-checker.importStrategy": "fromEnvironment",
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

`.vscode/extensions.json`:

```json
{
  "recommendations": [
    "charliermarsh.ruff",
    "ms-python.mypy-type-checker",
    "ms-python.python"
  ]
}
```

## Step 11 — Cheat sheet

Mention these to the user at the end of setup:

```bash
# run the dev server (hot reload)
uv run uvicorn <package_name>.main:app --reload --port 8000

# in another terminal — interactive docs
open http://localhost:8000/docs       # macOS
xdg-open http://localhost:8000/docs   # Linux

# raw OpenAPI for the frontend's openapi-typescript
curl -s http://localhost:8000/openapi.json | jq

# add a runtime dep
uv add <pkg>

# add a dev dep
uv add --dev <pkg>

# run anything in the venv without activating it
uv run pytest
uv run mypy src
uv run ruff check .
uv run ruff format .
```

If an ORM was chosen, Alembic is installed but **not** scaffolded — running `alembic init` writes a chunk of config the user usually wants to customise. When ready:

```bash
# scaffold migrations (one-time)
uv run alembic init alembic

# wire alembic to your Settings.database_url — edit alembic/env.py:
#     from <package_name>.config import get_settings
#     config.set_main_option("sqlalchemy.url", get_settings().database_url)

# create a migration after editing models
uv run alembic revision --autogenerate -m "<description>"

# apply pending migrations
uv run alembic upgrade head
```

Reminder: install your DB driver before any Alembic / app operation touches the DB:
```bash
# Postgres + async (sqlalchemy[asyncio] or sqlmodel)
uv add asyncpg

# SQLite (handy for tests + local dev)
uv add aiosqlite
```

## Step 12 — Verify

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest

# the app boots
uv run uvicorn <package_name>.main:app --port 8000 &
sleep 2
curl -s http://localhost:8000/healthz   # expect {"status":"ok"}
curl -s http://localhost:8000/openapi.json | jq '.openapi'  # expect "3.1.0"
kill %1
```

All four `uv run` commands must succeed. The curl checks confirm the server actually started — useful because a misconfigured CORS list or an import-time error in `config.py` would crash uvicorn before the first request.

## Step 13 — First commit

```bash
# Pull the canonical Python.gitignore (overwrites the one uv init
# scaffolded). github/gitignore is the upstream source of truth and
# tracks new tools/caches as they appear.
curl -sLo .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# Keep .env.example tracked. Python.gitignore's `.env` pattern matches
# only the literal `.env` file (not `.env.example`), but some forks
# use `.env*` — the explicit unignore is cheap insurance.
printf '\n# Tracked env template\n!.env.example\n' >> .gitignore

git init
git add -A
git commit -m "chore: initial FastAPI service scaffold"
```

`git init` (no `-b` flag) honours `init.defaultBranch` from the user's git config — works for `main`, `master`, or anything else without forcing a rename.

If a `gh` remote is desired, ask the user before creating it.

## Anti-patterns this skill is built to prevent

- **Hard-coding env values** in `config.py` defaults that should be required (database URLs, secret keys). Use `Field(...)` (no default) for required values so the boot fails fast on a missing env.
- **Reading `process.env`/`os.environ` directly** elsewhere in the code. Settings is the only entry point — keeps the surface auditable.
- **Module-level `app = FastAPI()` without a factory.** Tests can't isolate state, dependency overrides leak between tests. The `create_app()` factory is the cost of one indentation level and unlocks proper isolation.
- **Tight coupling of routers to the global `app`** via decorators at module import time. Use `APIRouter()` instances mounted by the factory. Same reason.
- **Logging via `print()`.** Ruff's `T20` already errors. Use the stdlib `logging` module or structlog.
- **Naive `datetime` in models.** `DTZ` already errors. Always `datetime.now(UTC)`.
- **Skipping `py.typed`**. Free file, real upside if anyone else ever imports this package.
- **Pinning runtime deps to exact versions** in `[project].dependencies`. Use lower bounds (`fastapi>=0.115`); reproducibility comes from `uv.lock`, not from your spec.
- **`# type: ignore`** without a code. The `ignore-without-code` error code is on; do not weaken it.
- **Relative imports**. `ban-relative-imports = "all"` is set; use absolute imports.

## Things this skill does NOT cover

- **Database drivers** (`asyncpg`, `psycopg`, `aiosqlite`, `aiomysql`, `aioodbc`, …). Pick yours once the deploy target is known and `uv add` it.
- **Alembic scaffolding**. The package is installed if you picked an ORM; running `alembic init` is mentioned in the cheat sheet but left for the user.
- **Authentication**. Out of scope — every project picks its model (OAuth2 + JWT, API keys, session cookies, NextAuth-on-the-frontend with a JWT verifier here, …).
- **Async DB session management**. The recipe depends on the ORM and driver; wire `sessionmaker` / `Depends(get_session)` per project.
- **Background tasks / workers**. `BackgroundTasks` for one-off post-response work works out of the box. For real workers (APScheduler in a separate process, Celery, RQ, Arq, Dramatiq, …) pick per project — the trenaldia.es backend uses an APScheduler-in-its-own-process pattern as a reference if you want one.
- **Containerisation**. The Dockerfile depends on the deploy target (Cloud Run, Fly.io, Hetzner VPS, K8s) — leave to the project.
- **Observability** (structlog, OpenTelemetry, Sentry). Pick per project; add when you have an alert destination.

## When this skill goes stale

- Check Python's release cycle (https://devguide.python.org/versions/). The "Pick when…" table needs to move when 3.15 lands (Oct 2026).
- FastAPI has been at 0.x since forever; if it finally cuts a 1.0, audit this skill for breaking changes.
- `pydantic-settings` 2.x is current; if it bumps to 3 with a config-schema change, the Settings template needs an update.
- SQLAlchemy 2.x is the modern baseline; if a 3.x lands with different `Mapped[...]` semantics or another async session API, update Step 4 and the cheat sheet.
- `uvicorn`'s `[standard]` extra changes contents occasionally; check `uv pip show uvicorn` if startup feels weird.
- If Alembic ever ships a uv-aware bootstrap that auto-wires `Settings.database_url`, replace the manual `env.py` editing instructions in Step 11.
