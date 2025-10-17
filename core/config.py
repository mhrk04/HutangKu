"""
Shared configuration settings for the Debt Management Portal
Loads environment variables from .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_BASE_URL: str = f"http://{API_HOST}:{API_PORT}"
    
    # MongoDB Configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "debt_management")
    MONGODB_COLLECTION: str = "debts"
    
    # Application Configuration
    APP_NAME: str = "HutangKu"
    APP_VERSION: str = "1.0.0"
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # Notification Settings
    DUE_DATE_WARNING_DAYS: int = int(os.getenv("DUE_DATE_WARNING_DAYS", "7"))

settings = Settings()