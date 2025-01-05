import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIROMENT: str = os.getenv("ENVIROMENT", "main")
    DEBUG: bool = ENVIROMENT == "dev"
    PUBLIC_DOMAIN: str = f"https://{'dev' if DEBUG else ''}api.czmatejt.me"
    APP_NAME: str = f"akkurim-server-{ENVIROMENT}"
    APP_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/v1"

    SUPERTOKENS_CONNECTION_URI: str = "http://supertokens:3567"
    API_DOMAIN: str = "http://localhost:8002"  # TODO setup reverse proxy with traefik
    WEBSITE_DOMAIN: str = (
        "http://localhost:3002"  # TODO setup reverse proxy with traefik
    )
    API_KEY: str = os.getenv("API_KEY", "none")
    DASHBOARD_ADMIN: str = "tajovsky.matej@gmail.com"

    DATABASE_URL: str = str(os.getenv("DATABASE_URL", "none"))
    MIN_CONNECTIONS: int = 1
    MAX_CONNECTIONS: int = 10

    # not related to settings but to pydantic
    model_config = {"case_sensitive": True}


settings = Settings()
print(settings.DEBUG)
