import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIROMENT: str = os.getenv("ENVIROMENT", "main")
    DEBUG: bool = ENVIROMENT == "dev"

    APP_NAME: str = f"akkurim-server-{ENVIROMENT}"
    APP_VERSION: str = "0.2.0"
    API_V1_PREFIX: str = "/v1"
    API_V2_PREFIX: str = "/v2"

    PUBLIC_DOMAIN: str = (
        f"https://api.akkurim.cz" if not DEBUG else "http://192.168.0.9:8000"
    )
    API_DOMAIN: str = (
        "https://api.akkurim.cz" if not DEBUG else "http://192.168.0.9:8000"
    )
    WEBSITE_DOMAIN: str = (
        "https://akkurim.cz" if not DEBUG else "http://192.168.0.9:3000"
    )

    API_KEY: str = os.getenv("API_KEY", "none")
    DASHBOARD_ADMIN: str = "tajovsky.matej@gmail.com"

    SUPERTOKENS_CONNECTION_URI: str = "http://supertokens:3567"

    IS_CAS_USERNAME: str = os.getenv("IS_CAS_USERNAME", "none")
    IS_CAS_PASSWORD: str = os.getenv("IS_CAS_PASSWORD", "none")
    IS_CAS_CLUB_ID: int = int(os.getenv("IS_CAS_CLUB_ID", "none"))

    # not related to settings but to pydantic
    model_config = {"case_sensitive": True}


settings = Settings()
