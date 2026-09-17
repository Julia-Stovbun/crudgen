import os
import subprocess
import sys

import pytest

from crudgen.core.generator import render_fastapi
from crudgen.core.loader import load_config

CONFIG = """entity: User
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
  score:
    type: float
    nullable: true
  created_at:
    type: datetime
    nullable: true
"""


def test_generated_app(tmp_path):
    cfg = tmp_path / "user.yaml"
    cfg.write_text(CONFIG)
    output = tmp_path / "app"
    result = subprocess.run(
        [sys.executable, "-m", "crudgen.cli", str(cfg), "--out", str(output)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert len(list(output.iterdir())) == 7
    script = """from fastapi.testclient import TestClient
from main import app
from db import engine
from models import Base, User
from schemas import UserCreate, UserRead
from sqlalchemy import inspect

assert 'users' in inspect(engine).get_table_names()
assert set(User.__table__.columns.keys()) == {'id', 'email', 'is_active', 'score', 'created_at'}
assert UserCreate.model_validate({'email': 'a@example.com'}).is_active is True
assert UserRead.model_validate(User(id=1, email='a@example.com', is_active=True)).id == 1
client = TestClient(app)
assert client.get('/health').json() == {'status': 'ok'}
assert client.get('/docs').status_code == 200
assert '/users/' in client.get('/openapi.json').json()['paths']
created = client.post('/users/', json={'email': 'a@example.com'})
assert created.status_code == 201, created.text
item = created.json()
assert item['is_active'] is True and item['id'] == 1
assert client.get('/users/').json() == [item]
assert client.get('/users/1').json() == item
updated = client.put('/users/1', json={'email': 'b@example.com', 'score': 1.5})
assert updated.status_code == 200 and updated.json()['score'] == 1.5
assert client.delete('/users/1').status_code == 204
assert client.get('/users/1').status_code == 404
"""
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{tmp_path / 'test.db'}"
    result = subprocess.run(
        [sys.executable, "-c", script], cwd=output, env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    with pytest.raises(FileExistsError):
        render_fastapi(load_config(str(cfg)), output)
