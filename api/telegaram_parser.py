from telethon import TelegramClient
from datetime import datetime
import asyncio

from config.config import TG_API_ID, TG_API_HASH

channels = [
    "rbc_news",
    "tass_agency"
]


async def parse_telegram(channel: str, count: int = 5):
    posts = []

    async with TelegramClient("session", TG_API_ID, TG_API_HASH) as client:
        async for message in client.iter_messages(channel, limit=count):

            text = message.text or ""

            post = {
                "id": f"tg_{channel}_{message.id}",
                "title": text[:80] if text else "Пост Telegram",
                "text": text,
                "source": {
                    "type": "telegram",
                    "name": channel,
                    "url": f"https://t.me/{channel}/{message.id}",
                    "author": "Telegram"
                },
                "time": {
                    "published_at": message.date.isoformat(),
                    "parsed_at": datetime.now().isoformat()
                }
            }

            posts.append(post)

    return posts