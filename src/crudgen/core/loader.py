from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from crudgen.core.config import EntityConfig


def load_config(path: str) -> EntityConfig:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {p}")

    data: Any
    if p.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    elif p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
    else:
        raise ValueError("Unsupported config extension. Use .yaml/.yml or .json")

    if not isinstance(data, dict):
        raise ValueError("Config root must be an object (mapping)")

    return EntityConfig.model_validate(data)
