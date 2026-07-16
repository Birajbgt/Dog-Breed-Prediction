from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "model_ready": "yes"}
