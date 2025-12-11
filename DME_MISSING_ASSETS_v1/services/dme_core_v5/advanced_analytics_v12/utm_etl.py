import logging
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import requests

from .config import get_settings
from .db import SessionLocal
from .models import UTMEvent, User

logger = logging.getLogger("dme_utm_etl")
settings = get_settings()


def fetch_raw_utm_events() -> List[Dict[str, Any]]:
    """Fetch raw UTM events from the configured analytics API."""
    base = settings.utm_analytics_api_base
    token = settings.utm_analytics_api_token
    if not base or not token:
        logger.warning("UTM analytics API not configured; skipping fetch")
        return []

    url = f"{base.rstrip('/')}/events"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, dict) and "events" in data:
        return list(data["events"])
    if isinstance(data, list):
        return data

    logger.warning("Unexpected UTM analytics payload shape: %s", type(data))
    return []


def normalize_event(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Map vendor-specific payload to the UTMEvent schema."""
    utm = raw.get("utm", {}) or {}

    ts_raw: Optional[str] = raw.get("timestamp")
    if ts_raw:
        try:
            occurred_at = datetime.fromisoformat(ts_raw)
        except Exception:
            occurred_at = datetime.utcnow()
    else:
        occurred_at = datetime.utcnow()

    return {
        "session_id": raw.get("session_id") or raw.get("client_id"),
        "occurred_at": occurred_at,
        "source": utm.get("source") or raw.get("utm_source"),
        "medium": utm.get("medium") or raw.get("utm_medium"),
        "campaign": utm.get("campaign") or raw.get("utm_campaign"),
        "term": utm.get("term") or raw.get("utm_term"),
        "content": utm.get("content") or raw.get("utm_content"),
        "landing_page": raw.get("landing_page"),
        "referrer": raw.get("referrer"),
        "email": raw.get("email"),
    }


def upsert_utm_events(events: Iterable[Dict[str, Any]]) -> int:
    """Write normalised UTM events and update User attribution where possible."""
    session = SessionLocal()
    created = 0
    try:
        for ev in events:
            email = ev.pop("email", None)
            user: Optional[User] = None

            if email:
                user = session.query(User).filter(User.email == email).first()
                if user:
                    user.utm_source = ev.get("source") or user.utm_source
                    user.utm_medium = ev.get("medium") or user.utm_medium
                    user.utm_campaign = ev.get("campaign") or user.utm_campaign
                    user.utm_term = ev.get("term") or user.utm_term
                    user.utm_content = ev.get("content") or user.utm_content

                    now = ev.get("occurred_at") or datetime.utcnow()
                    if user.first_touch_at is None:
                        user.first_touch_at = now
                    user.last_touch_at = now

            utm = UTMEvent(
                user=user,
                session_id=ev["session_id"],
                occurred_at=ev["occurred_at"],
                source=ev["source"],
                medium=ev["medium"],
                campaign=ev["campaign"],
                term=ev["term"],
                content=ev["content"],
                landing_page=ev["landing_page"],
                referrer=ev["referrer"],
            )
            session.add(utm)
            created += 1

        session.commit()
        logger.info("Inserted %d UTM events", created)
        return created
    finally:
        session.close()


def run_utm_etl() -> int:
    """End-to-end ETL: fetch -> normalise -> store."""
    raw = fetch_raw_utm_events()
    if not raw:
        logger.info("No UTM events fetched")
        return 0
    norm = [normalize_event(e) for e in raw]
    return upsert_utm_events(norm)


if __name__ == "__main__":
    run_utm_etl()
