import requests
from datetime import datetime
from config.config import VK_TOKEN, VK_VERSION

VK_API = "https://api.vk.com/method/wall.get"

def parse_vk(domain: str, count: int = 5):
    params = {
        "domain": domain,
        "count": count,
        "filter": "owner",
        "access_token": VK_TOKEN,
        "v": VK_VERSION
    }

    response = requests.get(VK_API, params=params)
    data = response.json()

    posts = []

    if "response" not in data:
        print("VK API error:", data)
        return posts

    for item in data["response"]["items"]:
        text = item.get("text", "")

        post = {
            "id": f"vk_{item['owner_id']}_{item['id']}",
            "title": text[:80] if text else "Пост VK",
            "text": text,
            "source": {
                "type": "vk",
                "name": domain,
                "url": f"https://vk.com/wall{item['owner_id']}_{item['id']}",
                "author": "VK"
            },
            "time": {
                "published_at": datetime.fromtimestamp(item["date"]).isoformat(),
                "parsed_at": datetime.now().isoformat()
            }
        }
        posts.append(post)

    return posts