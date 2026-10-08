# CRUDGen

CLI tool for generating a small runnable FastAPI CRUD project from a YAML or JSON schema.

## Features

Generates a SQLAlchemy model, Pydantic schemas, CRUD functions, FastAPI routes, SQLite setup, and an app entry point. Supported field types are `int`, `str`, `bool`, `float`, and `datetime`. One entity with an integer `id` is supported per project.

## Requirements

Python 3.11 or 3.12.

## Installation

```bash
python -m pip install .
```

## Usage

Save this as `user.yaml`:

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

Generate the project:

```bash
crudgen user.yaml --out generated
```

JSON configs use the same structure. Existing generated files are protected unless `--overwrite` is passed.

## Generated project

`generated/` contains `main.py`, `db.py`, `models.py`, `schemas.py`, `crud.py`, `router.py`, and `requirements.txt`.

```bash
cd generated
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`. The app uses `app.db` by default. Set `DATABASE_URL` to another SQLite URL to change its location.

## Development

```bash
python -m pip install -e '.[dev]'
pytest -q
ruff check .
```

## License

MIT
