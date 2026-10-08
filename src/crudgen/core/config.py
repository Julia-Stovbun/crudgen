from __future__ import annotations

import keyword
from typing import Literal

from pydantic import BaseModel, Field, model_validator

FieldType = Literal["int", "str", "bool", "float", "datetime"]


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///./app.db"


class FieldSpec(BaseModel):
    type: FieldType
    primary_key: bool = False
    unique: bool = False
    nullable: bool = False
    default: str | int | float | bool | None = None

    @model_validator(mode="after")
    def validate_field(self) -> FieldSpec:
        if self.primary_key and (self.nullable or self.default is not None):
            raise ValueError("primary key cannot be nullable or have a default")
        if self.default is not None:
            if self.type == "datetime":
                raise ValueError("datetime defaults are not supported")
            expected = {"str": str, "int": int, "float": (int, float), "bool": bool}[self.type]
            if not isinstance(self.default, expected) or (
                self.type in {"int", "float"} and isinstance(self.default, bool)
            ):
                raise ValueError(f"default must match field type {self.type}")
        return self


class EntityConfig(BaseModel):
    entity: str = Field(min_length=1)
    table: str = Field(min_length=1)
    fields: dict[str, FieldSpec] = Field(min_length=1)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @model_validator(mode="after")
    def validate_entity(self) -> EntityConfig:
        if (
            not self.entity.isidentifier()
            or keyword.iskeyword(self.entity)
            or self.entity in {"Base", "datetime"}
        ):
            raise ValueError("entity must be a non-reserved Python identifier")
        if not self.table.isidentifier() or keyword.iskeyword(self.table):
            raise ValueError("table must be a Python identifier")
        if any(
            not name.isidentifier()
            or keyword.iskeyword(name)
            or name in {"metadata", "registry"}
            or name.startswith("__")
            for name in self.fields
        ):
            raise ValueError("field names must be non-reserved Python identifiers")
        if "id" not in self.fields or not self.fields["id"].primary_key:
            raise ValueError("fields.id must have primary_key: true")
        if self.fields["id"].type != "int":
            raise ValueError("fields.id must have type: int")
        if any(spec.primary_key for name, spec in self.fields.items() if name != "id"):
            raise ValueError("only fields.id may be a primary key")
        if not self.db.url.startswith("sqlite:///"):
            raise ValueError("db.url must be a SQLite URL (sqlite:///...)")
        return self
