from pydantic import BaseSettings, EmailStr
from pathlib import Path
import os
from dotenv import load_dotenv
from logging import getLogger


log = getLogger(__name__)

root_dir = Path(__file__).resolve().parent.parent.parent
env_file = os.path.join(root_dir, ".env")


load_dotenv(env_file)


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "FAKE_SECRET")
    ALGORITHM: str = "HS256"
    MAIL_ADDRESS: EmailStr = os.getenv("EMAIL", "FAKE_EMAIL")
    MAIL_PASSWORD: str = os.getenv("PASSWORD", "FAKE_PASSWORD")
    MAIL_PORT: int = 587
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "FAKE_SERVER")
    DB_URI: str = os.getenv("DB_URI", "sqlite://db.sqlite3")


def get_settings():
    log.info("Loading settings")
    _settings = Settings()
    log.info("Settings loaded")
    return _settings


settings = get_settings()
