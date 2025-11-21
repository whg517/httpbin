from typing import List


class Settings:
    """Application settings"""

    # Application info
    APP_NAME: str = "httpbin"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "A simple HTTP Request & Response Service"

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Request limits
    MAX_DELAY_SECONDS: int = 10
    MAX_REDIRECT_COUNT: int = 10


settings = Settings()
