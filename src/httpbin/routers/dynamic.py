import asyncio
import secrets
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from ..config import settings
from ..utils import decode_base64, encode_base64

router = APIRouter(tags=["Dynamic Behavior"])


@router.get("/delay/{seconds}")
async def delay_response(seconds: int):
    """
    Delays responding for min(seconds, MAX_DELAY_SECONDS) seconds.
    """
    if seconds < 0:
        raise HTTPException(status_code=400, detail="Delay must be non-negative")

    # Cap the delay at configured maximum
    actual_delay = min(seconds, settings.MAX_DELAY_SECONDS)

    await asyncio.sleep(actual_delay)

    return {
        "delay": actual_delay,
        "requested": seconds,
        "message": f"Delayed response by {actual_delay} seconds",
    }


@router.get("/base64/{value}")
async def decode_base64_value(value: str):
    """Decodes a base64-encoded string"""
    decoded = decode_base64(value)
    return {"decoded": decoded, "original": value}


@router.post("/base64/encode")
async def encode_to_base64(data: dict):
    """Encodes input text to base64"""
    text = data.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="'text' field is required")

    encoded = encode_base64(text)
    return {"encoded": encoded, "original": text}


@router.get("/uuid")
async def generate_uuid():
    """Generates a random UUID"""
    return {"uuid": str(uuid.uuid4())}


@router.get("/bytes/{n}")
async def random_bytes(n: int):
    """Generates n random bytes"""
    if n < 1 or n > 102400:  # Max 100KB
        raise HTTPException(status_code=400, detail="n must be between 1 and 102400")

    random_data = secrets.token_bytes(n)
    return Response(content=random_data, media_type="application/octet-stream")
