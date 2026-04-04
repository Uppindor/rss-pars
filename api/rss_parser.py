import feedparser
from datetime import datetime

def parse_rss(url: str):
    feed = feedparser.parse(url)
    news = []

    for entry in feed.entries:
        text = (
            getattr(entry, "summary", None)
            or getattr(entry, "description", None)
            or getattr(entry, "title", "")
        )

        post = {
            "id": entry.get("id", entry.link),
            "title": entry.get("title", ""),
            "text": text,
            "source": {
                "type": "rss",
                "name": feed.feed.get("title", "RSS"),
                "url": entry.link,
                "author": entry.get("author", "")
            },
            "time": {
                "published_at": entry.get(
                    "published",
                    datetime.now().isoformat()
                ),
                "parsed_at": datetime.now().isoformat()
            }
        }

        news.append(post)

    return news