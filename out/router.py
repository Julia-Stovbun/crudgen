from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", summary="List users")
def list_users():
    return []


@router.post("/", summary="Create User")
def create_users():
    return {"status": "ok"}
