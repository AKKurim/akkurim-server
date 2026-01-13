from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ACTIVE_TENANTS: list[str] = ["kurim"]

    model_config = {"case_sensitive": True}


db_settings = Settings()
