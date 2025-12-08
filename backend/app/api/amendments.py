from fastapi import APIRouter, HTTPException
from app.core.amendments import get_deal_versions, compare_versions
from typing import List

router = APIRouter()

@router.get("/{base_deal_name}/versions")
def list_versions(base_deal_name: str):
    versions = get_deal_versions(base_deal_name)
    return {"versions": versions}

@router.get("/compare")
def compare(v1: str, v2: str):
    return compare_versions(v1, v2)

