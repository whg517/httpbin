from fastapi import APIRouter, Response, status

from httpbin.schemas import StatusResponse

router = APIRouter(tags=["Status Codes"])


@router.get("/status/{codes}")
@router.post("/status/{codes}")
@router.put("/status/{codes}")
@router.patch("/status/{codes}")
@router.delete("/status/{codes}")
async def status_codes(codes: str, response: Response):
    """
    Returns given HTTP Status code.
    Supports multiple comma-separated status codes (returns first one).
    """
    # Parse status codes (support comma-separated)
    code_list = [c.strip() for c in codes.split(",")]

    try:
        status_code = int(code_list[0])
    except ValueError:
        status_code = 400
        response.status_code = status_code
        return StatusResponse(code=status_code, message="Invalid status code")

    # Validate status code range
    if not (100 <= status_code < 600):
        status_code = 400
        response.status_code = status_code
        return StatusResponse(code=status_code, message="Status code out of range")

    response.status_code = status_code

    # Get status message
    try:
        message = status._status_code_to_phrase.get(status_code, "Unknown Status")
    except Exception:
        message = "Unknown Status"

    return StatusResponse(code=status_code, message=message)
