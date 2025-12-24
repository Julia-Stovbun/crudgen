from crudgen.core.generator import render_fastapi
from crudgen.core.loader import load_config


def test_generation_creates_files(tmp_path):
    cfg_path = tmp_path / "user.yaml"
    cfg_path.write_text(
        """
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
""".strip(),
        encoding="utf-8",
    )

    cfg = load_config(str(cfg_path))
    out_dir = tmp_path / "out"
    outputs = render_fastapi(cfg, out_dir=out_dir, overwrite=False)

    assert (out_dir / "models.py").exists()
    assert (out_dir / "schemas.py").exists()
    assert (out_dir / "router.py").exists()

    models = (out_dir / "models.py").read_text(encoding="utf-8")
    schemas = (out_dir / "schemas.py").read_text(encoding="utf-8")
    router = (out_dir / "router.py").read_text(encoding="utf-8")

    assert "class User" in models
    assert "class UserCreate" in schemas
    assert "router = APIRouter" in router

    assert len(outputs) == 3
