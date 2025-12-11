import logging
from datetime import datetime
from typing import Any, Dict, List

import requests

from .config import get_settings
from .db import SessionLocal
from .models import SeoRankSnapshot

logger = logging.getLogger("dme_seo_rank_tracker")
settings = get_settings()


def _iter_keywords() -> List[Dict[str, str]]:
    """Parse SEO_KEYWORDS env into a list of {keyword, url} dicts."""
    raw = settings.seo_keywords
    if not raw:
        return []

    pairs: List[Dict[str, str]] = []
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        if "|" in part:
            keyword, url = [p.strip() for p in part.split("|", 1)]
        else:
            keyword, url = part, ""
        pairs.append({"keyword": keyword, "url": url})
    return pairs


def fetch_rank_for_keyword(keyword: str, url: str) -> Dict[str, Any]:
    """Call the configured SEO API to retrieve rank for a given keyword+URL."""
    base = settings.seo_api_base
    key = settings.seo_api_key
    if not base or not key:
        logger.warning("SEO API not configured; returning empty rank for %s", keyword)
        return {"keyword": keyword, "url": url, "position": None, "search_volume": None}

    resp = requests.get(
        f"{base.rstrip('/')}/ranks",
        params={"keyword": keyword, "url": url},
        headers={"Authorization": f"Bearer {key}"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, dict):
        position = data.get("position") or data.get("rank")
        volume = data.get("search_volume")
    elif isinstance(data, list) and data:
        first = data[0]
        position = first.get("position") or first.get("rank")
        volume = first.get("search_volume")
    else:
        position = None
        volume = None

    return {
        "keyword": keyword,
        "url": url,
        "position": position,
        "search_volume": volume,
    }


def run_seo_rank_tracker() -> int:
    """Fetch and store SEO rank snapshots for all configured keywords."""
    pairs = _iter_keywords()
    if not pairs:
        logger.info("No SEO_KEYWORDS configured; nothing to track")
        return 0

    session = SessionLocal()
    created = 0
    try:
        for pair in pairs:
            result = fetch_rank_for_keyword(pair["keyword"], pair["url"])
            snap = SeoRankSnapshot(
                keyword=result["keyword"],
                url=result["url"],
                position=result["position"],
                search_volume=result["search_volume"],
                captured_at=datetime.utcnow(),
                source="seo_api",
            )
            session.add(snap)
            created += 1
        session.commit()
        logger.info("Recorded %d SEO rank snapshots", created)
        return created
    finally:
        session.close()


if __name__ == "__main__":
    run_seo_rank_tracker()
