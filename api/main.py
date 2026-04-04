from fastapi import FastAPI, Query
from datetime import datetime
import asyncio

from . import vk_parser, rss_parser, deduplication
from config.config import VK_GROUPS, RSS_FEEDS


api = FastAPI(title="News Parser Service")

cached_news = []
last_update = None

def collect_all_news(vk_groups=None, rss_feeds=None):
    vk_groups = vk_groups or VK_GROUPS
    rss_feeds = rss_feeds or RSS_FEEDS

    news = []

    # VK
    for domain in vk_groups:
        try:
            news += vk_parser.parse_vk(domain)
        except Exception as ex:
            print(f"Ошибка VK ({domain}): {ex}")

    # RSS
    for feed in rss_feeds:
        try:
            news += rss_parser.parse_rss(feed)
        except Exception as ex:
            print(f"Ошибка RSS ({feed}): {ex}")

    # Дедупликация
    news = deduplication.deduplicate(news)
    return news

# Фоновая задача каждые 5 минут
async def parser_loop():
    global cached_news, last_update
    while True:
        print("Парсинг новостей...")
        cached_news = collect_all_news()
        last_update = datetime.now()
        print(f"Обновлено: {last_update}")
        await asyncio.sleep(300)  # 5 минут

@api.on_event("startup")
async def startup_event():
    asyncio.create_task(parser_loop())

@api.get("/news")
def get_news():
    return {
        "news": cached_news,
        "count": len(cached_news),
        "last_update": last_update
    }

@api.get("/news/vk")
def get_vk_news(group_domain: str = Query(...)):
    news = collect_all_news(vk_groups=[group_domain])
    return {"news": news, "count": len(news), "group": group_domain}

@api.get("/news/rss")
def get_rss_news(url: str = Query(...)):
    news = collect_all_news(rss_feeds=[url])
    return {"news": news, "count": len(news), "feed": url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=True)