import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:

    """Class to store project and database configuration."""

    PROJECT_NAME:str = "Stockify-API"
    PROJECT_VERSION:str = "1.0"

    POSTGRES_DB:str = os.getenv('POSTGRES_DB')
    POSTGRES_USER:str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD:str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER:str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT:str = os.getenv('POSTGRES_PORT')

    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()