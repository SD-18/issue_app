import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment-specific configurations
ENV = os.getenv("ENV", "development")
load_dotenv(f".env.{ENV}")

def get_env_var(var_name, default=None):
    """Fetch an environment variable or raise an error if missing."""
    value = os.getenv(var_name, default)
    if value is None:
        raise RuntimeError(f"Environment variable {var_name} is not set!")
    return value

class Config:
    # Database Configuration
    DATABASE_URL = (
        f"mysql+mysqlconnector://{get_env_var('DB_USER')}:"
        f"{quote_plus(get_env_var('DB_PASSWORD'))}@"
        f"{get_env_var('DB_HOST')}:{get_env_var('DB_PORT', '3306')}/"
        f"{get_env_var('DB_NAME')}"
    )

    # JWT Configuration
    JWT_SECRET_KEY = get_env_var("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_TIME_MINUTES = int(os.getenv("JWT_EXPIRATION_TIME_MINUTES", 60))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # File Uploads
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/images")
    MAX_IMAGE_SIZE_KB = int(os.getenv("MAX_IMAGE_SIZE_KB", 5120))
    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Application Metadata
    APP_NAME = os.getenv("APP_NAME", "My App")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "My App Description")

    # Pagination
    DEFAULT_PAGE = int(os.getenv("DEFAULT_PAGE", 1))
    DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", 50))