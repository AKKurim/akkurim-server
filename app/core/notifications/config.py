from pydantic_settings import BaseSettings


class NotificationSettings(BaseSettings):
    ONESIGNAL_API_KEY: str = "your_default_onesignal_api_key"
    ONESIGNAL_APP_ID: str = "your_default_onesignal_app_id"

    model_config = {"case_sensitive": True}


notification_settings = NotificationSettings()
