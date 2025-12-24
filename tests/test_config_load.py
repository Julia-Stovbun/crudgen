from crudgen.core.loader import load_config


def test_load_config_ok(tmp_path):
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
""".strip(),
        encoding="utf-8",
    )

    cfg = load_config(str(cfg_path))
    assert cfg.entity == "User"
    assert cfg.table == "users"
    assert "id" in cfg.fields
    assert cfg.fields["id"].primary_key is True
