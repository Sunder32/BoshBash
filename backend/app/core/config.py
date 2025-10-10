"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import json
import os


class Settings(BaseSettings):
    """Application settings"""
    
    APP_NAME: str = "Rescue System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str = "mysql+pymysql://rescue_user:rescue_pass_2024_secure@localhost:3306/rescue_db?charset=utf8mb4"
    
    REDIS_URL: str = "redis://:rescue_redis_pass@localhost:6379/0"
    
    SECRET_KEY: str = "your-super-secret-key-change-in-production-min-32-chars-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    
    # Store as string, parse in property
    _cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Parse CORS origins from string"""
        value = self._cors_origins
        if not value:
            return ["http://localhost:3000"]
        
        # Try JSON format
        if value.startswith("["):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
        
        # Use comma-separated format
        return [origin.strip() for origin in value.split(",") if origin.strip()]


    
    MAPBOX_ACCESS_TOKEN: str = "your_mapbox_token_here"
    
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "noreply@rescue-system.ru"
    SMTP_PASSWORD: str = "your_email_password"
    EMAIL_FROM: str = "noreply@rescue-system.ru"
    
    SMS_API_KEY: str = "your_sms_api_key"
    SMS_API_URL: str = "https://sms-api.example.com"
    
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    DEFAULT_LATITUDE: float = 56.8587
    DEFAULT_LONGITUDE: float = 35.9176
    DEFAULT_ZOOM: int = 12
    
    RATE_LIMIT_PER_MINUTE: int = 60

    APK_DOWNLOAD_PATH: str = os.getenv("APK_DOWNLOAD_PATH", "downloads/sos-mobile-latest.apk")
    
    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'allow'  # Разрешить дополнительные поля из .env
        
        # Map environment variable CORS_ORIGINS to _cors_origins field
        fields = {
            '_cors_origins': {
                'env': 'CORS_ORIGINS'
            }
        }


settings = Settings()

if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)

if not os.path.exists("logs"):
    os.makedirs("logs")

apk_dir = os.path.dirname(settings.APK_DOWNLOAD_PATH)
if apk_dir and not os.path.exists(apk_dir):
    os.makedirs(apk_dir, exist_ok=True)
