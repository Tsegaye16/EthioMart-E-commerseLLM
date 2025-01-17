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

    def fetch_messages(self, channel_name, limit=100, min_id=None):
        """
        Fetch messages from a specific Telegram channel.
        :param channel_name: The channel to fetch messages from.
        :param limit: The maximum number of messages to fetch.
        :param min_id: Fetch messages with an ID greater than this value.
        :return: List of messages.
        """
        if min_id is None:
            min_id = 0  # Default to fetching all messages

        messages = []
        for message in self.client.iter_messages(channel_name, limit=limit, min_id=min_id):
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
        """
        Download media (images/documents) if available.
        :param message: A Telethon message object.
        :return: The path to the downloaded media or None if no media.
        """
        media_path = "./downloads"
        os.makedirs(media_path, exist_ok=True)

        if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
            pass#return self.client.download_media(message, file=media_path)
        return None

    def close(self):
        """Disconnect the Telegram client."""
        self.client.disconnect()
