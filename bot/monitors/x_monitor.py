"""
X (Twitter) API v2 monitor for high-signal Grok / xAI posts.
Uses Bearer Token (app-only) for reading.
"""

from __future__ import annotations

from typing import Any

import requests

from config import (
    X_BEARER_TOKEN,
    WATCH_ACCOUNTS,
    WATCH_ELON,
    POSTS_PER_ACCOUNT,
)
from utils.logger import get_logger
from utils.filters import is_high_signal

logger = get_logger("x_monitor")

BASE = "https://api.twitter.com/2"


class XMonitor:
    def __init__(self, bearer_token: str | None = None):
        self.bearer = bearer_token or X_BEARER_TOKEN
        if not self.bearer:
            raise ValueError("X_BEARER_TOKEN is required")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.bearer}",
                "User-Agent": "GrokatiBot/0.1",
            }
        )

    def _get(self, path: str, params: dict | None = None) -> dict:
        url = f"{BASE}{path}"
        resp = self.session.get(url, params=params, timeout=30)
        if resp.status_code != 200:
            logger.error("X API error %s: %s", resp.status_code, resp.text[:300])
            resp.raise_for_status()
        return resp.json()

    def get_user_id(self, username: str) -> str | None:
        data = self._get(
            f"/users/by/username/{username}",
            params={"user.fields": "id,username,name"},
        )
        return data.get("data", {}).get("id")

    def get_user_tweets(self, user_id: str, max_results: int = 15) -> list[dict]:
        params = {
            "max_results": min(max(5, max_results), 100),
            "tweet.fields": "created_at,public_metrics,referenced_tweets,entities,lang",
            "exclude": "retweets,replies",  # reduce noise at API level where possible
        }
        data = self._get(f"/users/{user_id}/tweets", params=params)
        return data.get("data") or []

    def fetch_high_signal_posts(self) -> list[dict[str, Any]]:
        """
        Collect high-signal posts from watched accounts.
        Returns a list of dicts with normalized fields + original post.
        """
        results: list[dict[str, Any]] = []
        accounts = list(WATCH_ACCOUNTS)
        if WATCH_ELON and "elonmusk" not in accounts:
            accounts.append("elonmusk")

        for username in accounts:
            try:
                logger.info("Fetching recent posts from @%s", username)
                user_id = self.get_user_id(username)
                if not user_id:
                    logger.warning("Could not resolve user_id for @%s", username)
                    continue

                tweets = self.get_user_tweets(user_id, max_results=POSTS_PER_ACCOUNT)
                logger.info("  → %d tweets returned by API for @%s", len(tweets), username)

                for tw in tweets:
                    if is_high_signal(tw, author_username=username):
                        results.append(
                            {
                                "id": tw["id"],
                                "text": tw.get("text", ""),
                                "created_at": tw.get("created_at"),
                                "author": username,
                                "url": f"https://x.com/{username}/status/{tw['id']}",
                                "raw": tw,
                            }
                        )
                    else:
                        logger.debug("  filtered out: %s…", (tw.get("text") or "")[:60])

            except Exception as e:
                logger.exception("Failed to fetch @%s: %s", username, e)

        # Deduplicate by post id
        seen = set()
        unique = []
        for item in results:
            if item["id"] not in seen:
                seen.add(item["id"])
                unique.append(item)

        logger.info("Total high-signal posts after filtering: %d", len(unique))
        return unique
