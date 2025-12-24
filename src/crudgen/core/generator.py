from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from crudgen.core.config import EntityConfig


@dataclass(frozen=True)
class RenderContext:
    entity: str
    table: str
    fields: list[tuple[str, Any]]


def _env() -> Environment:
    templates_dir = Path(__file__).parent / "templates"
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_fastapi(cfg: EntityConfig, out_dir: str | Path, overwrite: bool = False) -> list[Path]:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    ctx = RenderContext(
        entity=cfg.entity,
        table=cfg.table,
        fields=list(cfg.fields.items()),
    )

    env = _env()

    outputs: list[Path] = []
    mapping = {
        "fastapi/models.py.j2": "models.py",
        "fastapi/schemas.py.j2": "schemas.py",
        "fastapi/router.py.j2": "router.py",
    }

    for template_name, filename in mapping.items():
        target = out_path / filename
        if target.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing file: {target}")
        content = env.get_template(template_name).render(ctx=ctx)
        target.write_text(content.rstrip() + "\n", encoding="utf-8")
        outputs.append(target)

    return outputs
