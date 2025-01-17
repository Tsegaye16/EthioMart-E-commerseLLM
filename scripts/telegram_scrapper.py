from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

API_ID = os.getenv("API_ID")  # Read from .env
API_HASH = os.getenv("API_HASH")  # Read from .env
SESSION_NAME = 'scraper_session'

class TelegramScraper:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        self.client.start()

    def fetch_messages(self, channel_name, limit=100):
        """Fetch messages from a specific Telegram channel."""
        messages = []
        for message in self.client.iter_messages(channel_name, limit=limit):
            msg_data = {
                "id": message.id,
                "sender": message.sender_id,
                "timestamp": message.date.isoformat(),
                "text": message.message or "",
                "media": self._download_media(message),
            }
            messages.append(msg_data)
        return messages

    def _download_media(self, message):
        """Download media (images/documents) if available."""
        media_path = "./downloads"
        os.makedirs(media_path, exist_ok=True)

        if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
            return self.client.download_media(message, file=media_path)
        return None

    def close(self):
        self.client.disconnect()
