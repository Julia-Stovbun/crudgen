import json

import pytest
from pydantic import ValidationError

from crudgen.core.loader import load_config


@pytest.mark.parametrize("extension", ["yaml", "json"])
def test_load_config(tmp_path, extension):
    data = {
        "entity": "User",
        "table": "users",
        "fields": {"id": {"type": "int", "primary_key": True}, "email": {"type": "str"}},
    }
    path = tmp_path / f"user.{extension}"
    if extension == "json":
        path.write_text(json.dumps(data))
    else:
        path.write_text(
            "entity: User\ntable: users\nfields:\n"
            "  id:\n    type: int\n    primary_key: true\n"
            "  email:\n    type: str\n"
        )
    assert load_config(str(path)).entity == "User"


@pytest.mark.parametrize("field", ["bad-name", "class"])
def test_reject_invalid_field_name(tmp_path, field):
    path = tmp_path / "bad.json"
    path.write_text(
        json.dumps(
            {
                "entity": "User",
                "table": "users",
                "fields": {"id": {"type": "int", "primary_key": True}, field: {"type": "str"}},
            }
        )
    )
    with pytest.raises(ValidationError):
        load_config(str(path))
