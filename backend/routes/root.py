from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root() -> Dict[str, str]:
    return {
        "message": "Dog Breed Prediction API is running",
        "docs": "/docs",
        "health": "/health",
    }
