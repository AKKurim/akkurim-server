import os

from pydantic_settings import BaseSettings


class NotificationSettings(BaseSettings):
    ONESIGNAL_API_KEY: str = os.getenv("ONESIGNAL_API_KEY", "none")
    ONESIGNAL_APP_ID: str = os.getenv("ONESIGNAL_APP_ID", "none")
    ONESIGNAL_API_URL: str = "https://api.onesignal.com/notifications?c=push"

    model_config = {"case_sensitive": True}


notification_settings = NotificationSettings()
