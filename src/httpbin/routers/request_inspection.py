from fastapi import APIRouter, Request

from ..schemas import HeadersResponse, IPResponse

router = APIRouter(tags=["Request Inspection"])


@router.get("/headers", response_model=HeadersResponse)
async def get_headers(request: Request):
    """Returns the request headers"""
    return HeadersResponse(headers=dict(request.headers))


@router.get("/ip", response_model=IPResponse)
async def get_ip(request: Request):
    """Returns the requester's IP address"""
    origin = request.client.host if request.client else "unknown"

    # Check for forwarded IP
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        origin = forwarded_for.split(",")[0].strip()

    return IPResponse(origin=origin)


@router.get("/user-agent")
async def get_user_agent(request: Request):
    """Returns the user-agent header"""
    user_agent = request.headers.get("user-agent", "")
    return {"user-agent": user_agent}
