# crudgen — Config-driven FastAPI CRUD code generator (Lite)

Generate clean, editable FastAPI building blocks from a small YAML or JSON config.

No runtime magic.  
No hidden abstractions.  
You get plain Python files you can read, own, and modify.

---

## What this is

`crudgen` is a **config-first code generator** for FastAPI projects.

Given a small YAML or JSON config, it generates:

- SQLAlchemy model skeletons
- Pydantic schema skeletons
- FastAPI router skeletons

The generated code is **not a framework** and **not a runtime dependency**.  
It is meant to be copied into your project and edited freely.

---

## What Lite generates

From a single config file, Lite generates:

- `models.py` — SQLAlchemy model skeleton
- `schemas.py` — Pydantic schemas
- `router.py` — FastAPI router skeleton

---

## What Lite intentionally does NOT do

Lite does **not** generate:

- a runnable FastAPI app (`main.py`)
- database engine or session wiring
- real CRUD handlers
- authentication or permissions

Lite is designed to stop at **clean, readable building blocks**.

---

## Quickstart

### 1) Install (local / dev)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
```

Verify installation:

```bash
crudgen --help
```

---

### 2) Generate from example config

```bash
crudgen examples/user.yaml --out out --overwrite
```

Result:

```text
out/
  models.py
  schemas.py
  router.py
```

---

## Example config

`examples/user.yaml`

```yaml
entity: User
table: users

fields:
  id:
    type: int
    primary_key: true
  email:
    type: str
    unique: true
  is_active:
    type: bool
    default: true
```

---

## Design principles

- Config → Code, not runtime magic
- Generated code is fully editable
- No hidden behavior
- Deterministic output
- Minimal scope

This tool exists to save you from rewriting the same boilerplate again and again.

---

## Pro version (paid)

The Pro version adds:

- runnable FastAPI app (`main.py`)
- database wiring (SQLite / Postgres)
- real CRUD endpoints
- improved typing and defaults
- optional extras (auth, roles, relations, migrations)

👉 Pro version link: coming soon

---

## Development

Run tests:

```bash
pytest -q
```

Lint / format:

```bash
ruff check .
ruff format .
```

---

## License

MIT
