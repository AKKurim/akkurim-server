import requests

from app.core.config import settings

from .config import notification_settings


class NotificationService:
    def __init__(self):
        self.api_key = notification_settings.ONESIGNAL_API_KEY
        self.app_id = notification_settings.ONESIGNAL_APP_ID
        self.api_url = notification_settings.ONESIGNAL_API_URL
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Key {self.api_key}",
        }

    def send_notification_to_user(self, user_id_email: str, title: str, message: str):
        payload = {
            "app_id": self.app_id,
            "priority": 10,
            "contents": {"en": message, "cs": message},
            "headings": {"en": title, "cs": title},
            "target_channel": "push",
            "include_aliases": {
                "external_id": [user_id_email],
            },
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.status_code, response.reason, response.text

    def send_notification_to_all(self, title: str, message: str):
        if settings.DEBUG:
            self.send_notification_to_user("tajovsky.matej@gmail.com", title, message)
            print("DEBUG mode: Sent notification to test user instead of all users.")
            return
        payload = {
            "app_id": self.app_id,
            "priority": 10,
            "contents": {"en": message, "cs": message},
            "headings": {"en": title, "cs": title},
            "target_channel": "push",
            "included_segments": ["All"],
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.status_code, response.reason, response.text


notification_service = NotificationService()


def get_notification_service() -> NotificationService:
    return notification_service
