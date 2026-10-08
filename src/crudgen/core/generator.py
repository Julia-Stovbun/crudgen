from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, PackageLoader, StrictUndefined

from crudgen.core.config import EntityConfig

TEMPLATES = {
    "main.py.j2": "main.py",
    "db.py.j2": "db.py",
    "models.py.j2": "models.py",
    "schemas.py.j2": "schemas.py",
    "crud.py.j2": "crud.py",
    "router.py.j2": "router.py",
    "requirements.txt.j2": "requirements.txt",
}


def render_fastapi(cfg: EntityConfig, out_dir: str | Path, overwrite: bool = False) -> list[Path]:
    out_path = Path(out_dir)
    targets = [out_path / name for name in TEMPLATES.values()]
    if not overwrite:
        existing = next((target for target in targets if target.exists()), None)
        if existing:
            raise FileExistsError(f"Refusing to overwrite existing file: {existing}")
    env = Environment(
        loader=PackageLoader("crudgen.core", "templates"),
        autoescape=False,
        trim_blocks=False,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    )
    env.filters["pyrepr"] = repr
    field_types = {spec.type for spec in cfg.fields.values()}
    sql_imports = [
        sqlalchemy_type
        for field_type, sqlalchemy_type in (
            ("bool", "Boolean"),
            ("datetime", "DateTime"),
            ("float", "Float"),
            ("int", "Integer"),
            ("str", "String"),
        )
        if field_type in field_types
    ]
    rendered = [
        env.get_template(template)
        .render(cfg=cfg, field_types=field_types, sql_imports=sql_imports)
        .rstrip()
        + "\n"
        for template in TEMPLATES
    ]
    out_path.mkdir(parents=True, exist_ok=True)
    for target, content in zip(targets, rendered, strict=True):
        target.write_text(content, encoding="utf-8")
    return targets
