from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

"""
This module contains the configuration settings for the API, loaded from environment
variables or a .env file.
"""


class Settings(BaseSettings):
    """API Configuration Settings"""

    # --- Database ---
    DATABASE_URL: str = Field(
        ..., description="Sync PostgreSQL connection URL (e.g., for migrations)"
    )
    POOL_SIZE: int = Field(
        10, description="Number of connections to keep open in the pool"
    )
    MAX_OVERFLOW: int = Field(
        20, description="Maximum number of connections allowed beyond pool_size"
    )
    POOL_TIMEOUT: int = Field(
        30, description="Timeout in seconds for acquiring a connection from the pool"
    )
    POOL_RECYCLE: int = Field(
        1800,
        description="Recycle connections after this many seconds (e.g., 30 minutes)",
    )

    GEMINI_API_KEY: str = Field(..., description="API Key for Google Gemini services")

    model_config = SettingsConfigDict(
        env_file=".env",  
        env_file_encoding="utf-8",
        extra="ignore",  
        case_sensitive=False,  
    )

settings = Settings()  # type:ignore
