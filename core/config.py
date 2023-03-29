import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the Flask app"""

    # Flask Config
    FLASK_DEBUG = bool(os.getenv('FLASK_DEBUG', 1))
    TESTING = bool(os.getenv('FLASK_TESTING', 0))

    # Cache settings
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST', None)
    CACHE_REDIS_PORT = os.getenv('CACHE_REDIS_PORT', None)
    CACHE_REDIS_SOCK = os.getenv('CACHE_REDIS_SOCK', None)

    # RQ settings
    RQ_REDIS_URL = os.getenv('RQ_REDIS_URL')

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Passcode for updating data
    UPDATE_DATA_PASSCODE = os.getenv('UPDATE_DATA_PASSCODE', 'passcode')
