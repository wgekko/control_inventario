import requests

class WebhookService:
    @staticmethod
    def send_alert(webhook_url: str, message: str) -> bool:
        """Envía una notificación HTTP POST a un Webhook (ej. Telegram Bot, Slack, Discord)."""
        if not webhook_url or not webhook_url.startswith("http"):
            return False
        try:
            payload = {"content": message, "text": message}
            response = requests.post(webhook_url, json=payload, timeout=5)
            return response.status_code in [200, 201, 204]
        except Exception as e:
            print(f"Error enviando webhook: {e}")
            return False