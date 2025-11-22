from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .config import settings
from .routers import (
    dynamic_router,
    http_methods_router,
    request_inspection_router,
    response_formats_router,
    status_codes_router,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Include routers
    app.include_router(http_methods_router)
    app.include_router(status_codes_router)
    app.include_router(request_inspection_router)
    app.include_router(response_formats_router)
    app.include_router(dynamic_router)

    # Root endpoint
    @app.get("/")
    async def root():
        """Redirect to API documentation"""
        return RedirectResponse(url="/docs")

    return app


# Create the app instance
app = create_app()


def main():
    """Run the application with uvicorn"""
    import uvicorn

    uvicorn.run(
        "httpbin.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
