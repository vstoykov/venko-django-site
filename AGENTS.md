# Agent Workflow & Architecture Guide (`AGENTS.md`)

This document defines architectural standards, environment setup, and operational workflows for automated coding agents and contributors modifying the `venko-django-site` repository.

---

## 1. Overview & Technology Stack

* **Project**: Personal website and blog ([`venelin-site`](./pyproject.toml)).
* **Python Runtime**: Python `>= 3.13` (Current environment: Python 3.14).
* **Core Framework**: Django `6.1` (tested against Django 5.2, 6.0, 6.1, and master via Tox).
* **Package & Environment Manager**: [`uv`](https://docs.astral.sh/uv/) using [`pyproject.toml`](./pyproject.toml) and [`uv.lock`](./uv.lock).
* **Task Runner**: [`just`](./justfile).
* **Key Dependencies**:
  * Rich-text editing: `django-prose-editor`
  * Media & image processing: `django-imagekit`, `pillow`
  * Cloud storage: `django-storages[google]` (Google Cloud Storage)
  * Social auth: `social-auth-app-django`
  * Code highlighting: `pygments`
  * Database utilities: `dj-database-url`, `psycopg` (PostgreSQL)

---

## 2. Repository Layout

```
.
├── justfile                     # Task automation recipes
├── pyproject.toml               # Project metadata & dependencies
├── uv.lock                      # Locked dependency graph
├── tox.ini                      # Multi-Python / multi-Django test matrix & pytest config
├── manage.py                    # Django management script
├── Dockerfile                   # Multi-stage production container build
├── compose.yaml                 # Local & containerized development orchestration
├── kube-deployment.yaml         # Kubernetes/Podman deployment manifest
├── data/                        # Local database (site.db), media, and collected static
└── venelin/                     # Core application package
    ├── blog/                    # Blog posts, categories, RSS/Atom feeds, markdown rendering
    ├── gallery/                 # Photo galleries, image upload handler, AJAX endpoints
    ├── links/                   # Curated links & bookmarks
    ├── pages/                   # Flatpage content management with prose editor
    ├── syntaxhighlighter/       # Pygments code formatting utilities
    ├── settings/                # Environment-specific settings modules
    ├── locale/                  # i18n translation catalogs (Bulgarian 'bg')
    ├── templates/               # Global HTML templates
    └── static/                  # Static assets (CSS, JS, images)
```

---

## 3. Settings Hierarchy & Configuration

Django settings are split into modular configurations located in [`venelin/settings/`](./venelin/settings):

* [`common.py`](./venelin/settings/common.py): Base settings shared across all environments.
* [`dev.py`](./venelin/settings/dev.py): Development profile. Uses local SQLite (`data/site.db`) and Django Debug Toolbar.
* [`local.py`](./venelin/settings/local.py): Optional, unversioned local overrides (ignored by git, automatically imported by `dev.py` and `production.py`).
* [`test.py`](./venelin/settings/test.py): Test runner profile. Extends `dev.py`, forces local `FileSystemStorage` (ensuring tests never hit Google Cloud Storage even if enabled in `local.py`).
* [`production.py`](./venelin/settings/production.py): Production profile. Enforces secret keys, PostgreSQL, GCS storage, and SSL flags.
* [`staging.py`](./venelin/settings/staging.py): Production-like profile with optional debug mode.

> **Environment Variables**:
> - `DJANGO_ENV`: Controls which settings module is loaded (`dev`, `production`, `staging`, `test`). Defaults to `dev`.
> - `DJANGO_SECRET_KEY`: Secret key required for production / staging.
> - `DATABASE_URL`: Supported via `dj-database-url`.

---

## 4. Operational Commands

Agents should execute commands using `just` or `uv run`:

| Goal | Command | Description |
|------|---------|-------------|
| **Run test suite** | `just test` | Collects static, compiles translations, runs `pytest` |
| **Direct pytest** | `uv run -m pytest` | Runs test suite using [`tox.ini`](./tox.ini) configuration |
| **Run dev server** | `just runserver` | Compiles messages, migrates, and runs Django dev server |
| **Database migration** | `just migrate` | Applies pending migrations (`manage.py migrate`) |
| **Generate migrations** | `uv run manage.py makemigrations` | Generates schema migrations for modified models |
| **Compile translations** | `just compilemessages` | Compiles `.po` files to `.mo` (ignoring `.venv`/`.tox`) |
| **Extract translations** | `just makemessages` | Updates `.po` catalog for Bulgarian (`bg`) locale |
| **Collect static files** | `just collectstatic` | Gathers assets into `data/static` (`--no-input`) |
| **Django shell** | `just shell` | Interactive shell (`manage.py shell_plus`) |
| **Upgrade dependencies**| `just upgrade-deps` | Updates locks via `uv lock --upgrade` |

---

## 5. Workflow for Making Modifications

When implementing bug fixes, improvements, or features, adhere to the following workflow:

### Step 1: Pre-Change Inspection
1. Review relevant models, views, templates, or settings.
2. Confirm the current test suite passes before making changes:
   ```bash
   just test
   ```

### Step 2: Implementation Guidelines
* **Python Style**:
  * Target Python 3.13+ syntax (f-strings, modern typing, standard `super()` calls).
  * Line length: Ruff configured for 100 characters ([`pyproject.toml`](./pyproject.toml)), Flake8 configured for 120 ([`tox.ini`](./tox.ini)).
* **Models & Migrations**:
  * When altering models in `venelin/blog/`, `venelin/gallery/`, `venelin/links/`, etc., create migrations immediately:
    ```bash
    uv run manage.py makemigrations
    ```
  * Never manually edit existing applied migration files unless specifically performing an approved squash/backfill.
* **Internationalization (i18n)**:
  * Any user-facing strings must be wrapped in `gettext_lazy` (`_('...')`).
  * If new translatable strings are added, update and compile catalogs:
    ```bash
    just makemessages
    just compilemessages
    ```
* **Static Assets**:
  * Changes to CSS/JS inside `venelin/static/` or template assets should be verified with `just collectstatic`.
* **Testing Isolation**:
  * Never write tests that require live external cloud connections (Google Cloud, OAuth providers, external DBs).
  * Use Django's `TestCase` or pytest fixtures with the test settings (`venelin.settings.test`).

### Step 3: Verification
1. Run full tests:
   ```bash
   just test
   ```
2. For targeted unit testing:
   ```bash
   uv run -m pytest venelin/blog/tests.py
   uv run -m pytest venelin/gallery/test.py
   ```
3. Check code formatting & linting:
   ```bash
   uv run ruff check venelin/
   ```

---

## 6. Containers & Deployment

* **Docker Build**:
  * Built using a multi-stage `Dockerfile`:
    - Stage 1 (`build`): Installs dependencies with `uv sync --frozen --no-dev`.
    - Stage 2 (`production`): Copies runtime virtualenv, executes build-time `collectstatic` and `compilemessages`, runs non-root (`www-data:www-data`).
* **Docker Compose**:
  * [`compose.yaml`](./compose.yaml) provides watch mode for file synchronization and automated container reload.
* **Podman / Kubernetes**:
  * Supports `podman kube play` via [`kube-deployment.yaml`](./kube-deployment.yaml) and [`kube-secrets.yaml`](./kube-secrets.yaml).
