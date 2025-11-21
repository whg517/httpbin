from fastapi import APIRouter, Request
from ..schemas import RequestInfo
from ..utils import get_request_data

router = APIRouter(tags=["HTTP Methods"])


@router.get("/get", response_model=RequestInfo)
async def get_method(request: Request):
    """Returns GET request data"""
    return await get_request_data(request)


@router.post("/post", response_model=RequestInfo)
async def post_method(request: Request):
    """Returns POST request data"""
    return await get_request_data(request)


@router.put("/put", response_model=RequestInfo)
async def put_method(request: Request):
    """Returns PUT request data"""
    return await get_request_data(request)


@router.patch("/patch", response_model=RequestInfo)
async def patch_method(request: Request):
    """Returns PATCH request data"""
    return await get_request_data(request)


@router.delete("/delete", response_model=RequestInfo)
async def delete_method(request: Request):
    """Returns DELETE request data"""
    return await get_request_data(request)
