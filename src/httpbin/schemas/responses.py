from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field


class RequestInfo(BaseModel):
    """Request information response model"""
    model_config = ConfigDict(populate_by_name=True)

    args: Dict[str, Any] = {}
    data: str = ""
    files: Dict[str, Any] = {}
    form: Dict[str, Any] = {}
    headers: Dict[str, str] = {}
    json_data: Optional[Any] = Field(None, alias="json")
    method: str
    origin: str
    url: str


class StatusResponse(BaseModel):
    """Status code response model"""
    code: int
    message: str


class HeadersResponse(BaseModel):
    """Headers response model"""
    headers: Dict[str, str]


class IPResponse(BaseModel):
    """IP address response model"""
    origin: str
