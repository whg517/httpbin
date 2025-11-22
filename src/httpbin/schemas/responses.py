from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RequestInfo(BaseModel):
    """Request information response model"""

    model_config = ConfigDict(populate_by_name=True)

    args: dict[str, Any] = {}
    data: str = ""
    files: dict[str, Any] = {}
    form: dict[str, Any] = {}
    headers: dict[str, str] = {}
    json_data: Any | None = Field(None, alias="json")
    method: str
    origin: str
    url: str


class StatusResponse(BaseModel):
    """Status code response model"""

    code: int
    message: str


class HeadersResponse(BaseModel):
    """Headers response model"""

    headers: dict[str, str]


class IPResponse(BaseModel):
    """IP address response model"""

    origin: str
