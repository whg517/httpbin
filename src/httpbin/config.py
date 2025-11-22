class Settings:
    """Application settings"""

    # Application info
    APP_NAME: str = "httpbin"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "A simple HTTP Request & Response Service"

    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Request limits
    MAX_DELAY_SECONDS: int = 10
    MAX_REDIRECT_COUNT: int = 10


settings = Settings()
