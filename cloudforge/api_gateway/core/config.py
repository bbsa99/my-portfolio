# CloudForge API Gateway - Configuration

"""
Pydantic-based configuration management for the API Gateway.

All settings are loaded from environment variables with sensible defaults.
Use .env file for local development and CI/CD for production settings.
"""

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable loading."""
    
    model_config = SettingsConfigDict(
        env_prefix="CF_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    app_name: str = Field(default="CloudForge-API-Gateway", alias="APP_NAME")
    debug: bool = Field(default=False, alias="DEBUG")
    version: str = Field(default="1.0.0", alias="VERSION")
    
    # Server configuration
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # CORS configuration
    cors_origins: list = Field(default=["http://localhost:3000"], alias="CORS_ORIGINS")
    cors_methods: list = Field(default=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"], alias="CORS_METHODS")
    cors_headers: list = Field(default=["*"], alias="CORS_HEADERS")
    
    # JWT Authentication
    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, alias="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Database
    postgres_dsn: str = Field(alias="POSTGRES_DSN")
    postgres_pool_min: int = Field(default=1, alias="POSTGRES_POOL_MIN")
    postgres_pool_max: int = Field(default=10, alias="POSTGRES_POOL_MAX")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    
    # Rate limiting
    rate_limit_default: str = Field(default="100/minute", alias="RATE_LIMIT_DEFAULT")
    rate_limit_auth: str = Field(default="10/minute", alias="RATE_LIMIT_AUTH")
    
    # Security
    allowed_hosts: list = Field(default=["localhost", "127.0.0.1", "::1"], alias="ALLOWED_HOSTS")
    
    # Service URLs
    catalog_service_url: str = Field(default="http://catalog:8001", alias="CATALOG_SERVICE_URL")
    orders_service_url: str = Field(default="http://orders:8002", alias="ORDERS_SERVICE_URL")
    
    # Feature flags
    feature_auth_enabled: bool = Field(default=True, alias="FEATURE_AUTH_ENABLED")
    feature_rate_limiting: bool = Field(default=True, alias="FEATURE_RATE_LIMITING")
    feature_metrics: bool = Field(default=True, alias="FEATURE_METRICS")
    
    @validator("jwt_secret_key")
    def jwt_key_must_be_long(cls, v):
        """Validate JWT secret key length."""
        if len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("postgres_dsn", pre=True)
    def assemble_postgres_dsn(cls, v, values):
        """Assemble PostgreSQL DSN from individual components if not provided."""
        if v:
            return v
        required = ["POSTGRESS_USER", "POSTGRESS_PASSWORD", "POSTGRESS_HOST", "POSTGRESS_DBNAME"]
        for r in required:
            if r not in values:
                raise ValueError(f"Missing required DB component: {r}")
        return f"postgresql+asyncpg://{values['POSTGRESS_USER']}:{values['POSTGRESS_PASSWORD']}@{values['POSTGRESS_HOST']}:5432/{values['POSTGRESS_DBNAME']}"
    
    model_config = SettingsConfigDict(
        env_prefix="CF_",
        extra="ignore",
    )


# Singleton instance
settings = Settings()


def get_settings():
    """Get the application settings instance."""
    return settings