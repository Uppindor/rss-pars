import hashlib

def get_hash(text: str) -> str:
    return hashlib.md5((text or "").encode()).hexdigest()

def deduplicate(news: list):
    seen = set()
    result = []
    for n in news:
        h = get_hash(n.get("text") or n.get("title"))
        if h not in seen:
            seen.add(h)
            result.append(n)
    return result