from urllib.parse import urlparse


def get_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def clean_text(text: str, max_length: int = 5000) -> str:
    if not text:
        return ""

    text = " ".join(text.split())

    return text[:max_length]


def prepare_source(source: dict) -> dict:
    url = source.get("url", "")
    source_type = classify_source(url)

    return {
        "title": source.get("title", "Untitled"),
        "url": url,
        "content": clean_text(
            source.get("content", "")
        ),
        "relevance_score": source.get(
            "score",
            source.get("relevance_score", 0.0)
        ),
        "source_type": source_type,
        "source_quality": get_source_quality(
            source_type
        ),
        "domain": get_domain(url)
    }


def classify_source(url: str) -> str:
    domain = get_domain(url)

    if domain.endswith(".gov"):
        return "government"

    if domain.endswith(".edu"):
        return "academic_institution"

    if domain in {
        "reuters.com",
        "apnews.com",
        "bbc.com",
        "nytimes.com",
        "theguardian.com"
    }:
        return "news"

    if domain == "reddit.com":
        return "social"

    if domain in {
        "facebook.com",
        "x.com",
        "twitter.com",
        "tiktok.com",
        "instagram.com"
    }:
        return "social"

    if domain.endswith(".org"):
        return "organization"

    return "general"

def get_source_quality(source_type: str) -> float:
    quality_scores = {
        "government": 0.95,
        "academic_institution": 0.90,
        "news": 0.85,
        "organization": 0.75,
        "general": 0.60,
        "social": 0.30,
    }

    return quality_scores.get(source_type, 0.50)

def filter_sources(sources: list[dict], max_sources: int = 6) -> list[dict]:
    filtered = []

    seen_urls = set()
    seen_domains = set()

    sorted_sources = sorted(
        sources,
        key=lambda source: source.get("relevance_score", 0.0),
        reverse=True
    )

    for source in sorted_sources:
        url = source.get("url", "")
        domain = source.get("domain", "")

        if not url or url in seen_urls:
            continue

        if not source.get("content"):
            continue

        if source.get("relevance_score", 0.0) < 0.30:
            continue

        # Avoid flooding Gemini with many results
        # from the exact same website.
        if domain in seen_domains:
            continue

        filtered.append(source)

        seen_urls.add(url)
        seen_domains.add(domain)

        if len(filtered) >= max_sources:
            break

    return filtered