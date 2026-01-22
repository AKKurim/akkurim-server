import os

from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    ACTIVE_TENANTS: list[str] = ["kurim"]
    DATABASE_URL: str = str(os.getenv("DATABASE_URL", "none"))

    model_config = {"case_sensitive": True}


db_settings = DBSettings()
