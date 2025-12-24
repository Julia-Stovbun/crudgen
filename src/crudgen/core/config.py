from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


FieldType = Literal["int", "str", "bool", "float", "datetime"]


class FieldSpec(BaseModel):
    type: FieldType
    primary_key: bool = False
    unique: bool = False
    nullable: bool = True
    default: Any | None = None

    @model_validator(mode="after")
    def _validate_pk(self) -> "FieldSpec":
        # pk обычно не nullable (и это ожидаемо почти везде)
        if self.primary_key:
            self.nullable = False
        return self


class EntityConfig(BaseModel):
    entity: str = Field(..., min_length=1, description="Entity class name, e.g. User")
    table: str = Field(..., min_length=1, description="DB table name, e.g. users")
    fields: dict[str, FieldSpec] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _validate_entity(self) -> "EntityConfig":
        if not self.fields:
            raise ValueError("fields must not be empty")
        if "id" not in self.fields:
            raise ValueError("fields must contain 'id'")
        if not self.fields["id"].primary_key:
            raise ValueError("fields.id must have primary_key: true")
        return self
