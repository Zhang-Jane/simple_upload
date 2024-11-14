from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.common.path_conf import BasePath


class Settings(BaseSettings):
    """Global Settings"""
    # 项目的名称
    PROJECT_NAME: str = "file_system"
    model_config = SettingsConfigDict(env_file=f'{BasePath}/.env', env_file_encoding='utf-8', extra='ignore')

    # Env Config
    ENVIRONMENT: Literal['dev', 'pro']

    # Env MySQL
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    # Env Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int

    # Env Token
    TOKEN_SECRET_KEY: str  # 密钥 secrets.token_urlsafe(32)

    # Env Opera Log
    OPERA_LOG_ENCRYPT_SECRET_KEY: str  # 密钥 os.urandom(32), 需使用 bytes.hex() 方法转换为 str

    # FastAPI
    API_V1_STR: str = '/api/v1'
    TITLE: str = 'FastAPI'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = 'FastAPI Best Architecture'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi'

    @model_validator(mode='before')
    @classmethod
    def validate_openapi_url(cls, values):
        if values['ENVIRONMENT'] == 'pro':
            values['OPENAPI_URL'] = None
        return values

    # Static Server
    STATIC_FILES: bool = False

    # Location Parse
    LOCATION_PARSE: Literal['online', 'offline', 'false'] = 'offline'

    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Shanghai'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # Limiter
    LIMITER_REDIS_PREFIX: str = f'{PROJECT_NAME}_limiter'

    # MySQL
    MYSQL_ECHO: bool = False
    MYSQL_DATABASE: str = 'file_system'
    MYSQL_CHARSET: str = 'utf8mb4'

    # Redis
    REDIS_TIMEOUT: int = 5

    # Log
    LOG_LEVEL: str = 'INFO'
    LOG_FORMAT: str = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | <lvl>{message}</>'
    LOG_STDOUT_FILENAME: str = f'{PROJECT_NAME}_access.log'
    LOG_STDERR_FILENAME: str = f'{PROJECT_NAME}_error.log'

    # Middleware
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_ACCESS: bool = True





@lru_cache
def get_settings() -> Settings:
    """获取全局配置"""
    return Settings()


# 创建配置实例
settings = get_settings()
