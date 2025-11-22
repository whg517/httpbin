from httpbin.routers.dynamic import router as dynamic_router
from httpbin.routers.http_methods import router as http_methods_router
from httpbin.routers.request_inspection import router as request_inspection_router
from httpbin.routers.response_formats import router as response_formats_router
from httpbin.routers.status_codes import router as status_codes_router

__all__ = [
    "http_methods_router",
    "status_codes_router",
    "request_inspection_router",
    "response_formats_router",
    "dynamic_router",
]
