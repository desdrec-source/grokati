"""
X (Twitter) API v2 monitor for high-signal Grok / xAI posts.
Uses Bearer Token (app-only) for reading.
Includes attached media URLs when present.
Also runs a recent search across the watch list + Grok keywords
so quote-tweets are not lost under a busy timeline.
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

WATCH_SEARCH = (
    "(from:grok OR from:xai OR from:elonmusk OR from:bot OR "
    "from:mattyp OR from:leerob OR from:Baconbrix OR from:cursor_ai OR from:LouiseGiam) "
    "(Grok OR xAI OR x.ai OR Imagine OR \"Grok Bot\" OR \"Grok Build\" "
    "OR SuperGrok OR Foundry OR Library)"
)


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

    def get_user_tweets(
        self, user_id: str, max_results: int = 15
    ) -> tuple[list[dict], dict[str, dict]]:
        params = {
            "max_results": min(max(5, max_results), 100),
            "tweet.fields": "created_at,public_metrics,referenced_tweets,entities,lang,attachments",
            "expansions": "attachments.media_keys",
            "media.fields": "url,preview_image_url,type,alt_text,width,height",
            "exclude": "retweets,replies",
        }
        data = self._get(f"/users/{user_id}/tweets", params=params)
        tweets = data.get("data") or []
        media_list = (data.get("includes") or {}).get("media") or []
        media_by_key = {m["media_key"]: m for m in media_list if "media_key" in m}
        return tweets, media_by_key

    @staticmethod
    def _extract_media(tw: dict, media_by_key: dict[str, dict]) -> list[dict[str, Any]]:
        keys = (tw.get("attachments") or {}).get("media_keys") or []
        out: list[dict[str, Any]] = []
        for key in keys:
            m = media_by_key.get(key)
            if not m:
                continue
            mtype = m.get("type")
            url = None
            if mtype == "photo":
                url = m.get("url")
                if not url:
                    continue
            elif mtype in ("video", "animated_gif"):
                url = m.get("preview_image_url") or ""
            else:
                continue
            out.append(
                {
                    "type": mtype,
                    "url": url,
                    "alt": m.get("alt_text") or "",
                    "width": m.get("width"),
                    "height": m.get("height"),
                }
            )
        return out

    def _item_from_tweet(
        self, tw: dict, username: str, media_by_key: dict[str, dict]
    ) -> dict[str, Any]:
        media = self._extract_media(tw, media_by_key)
        return {
            "id": tw["id"],
            "text": tw.get("text", ""),
            "created_at": tw.get("created_at"),
            "author": username,
            "url": f"https://x.com/{username}/status/{tw['id']}",
            "media": media,
            "has_video": any(
                (m.get("type") or "").lower() in ("video", "animated_gif") for m in media
            ),
            "raw": tw,
        }

    def fetch_tweet_by_id(self, tweet_id: str) -> dict[str, Any] | None:
        tid = str(tweet_id).strip()
        params = {
            "tweet.fields": "created_at,public_metrics,referenced_tweets,entities,lang,attachments,author_id",
            "expansions": "attachments.media_keys,author_id",
            "media.fields": "url,preview_image_url,type,alt_text,width,height",
            "user.fields": "username,name",
        }
        data = self._get(f"/tweets/{tid}", params=params)
        tw = data.get("data")
        if not tw:
            logger.warning("No tweet data for id %s", tid)
            return None

        includes = data.get("includes") or {}
        media_list = includes.get("media") or []
        media_by_key = {m["media_key"]: m for m in media_list if "media_key" in m}
        users = {u["id"]: u for u in (includes.get("users") or []) if "id" in u}
        author_id = tw.get("author_id")
        username = (users.get(author_id) or {}).get("username") or "unknown"
        return self._item_from_tweet(tw, username, media_by_key)

    def search_watchlist(self) -> list[dict[str, Any]]:
        params = {
            "query": WATCH_SEARCH,
            "max_results": 25,
            "tweet.fields": "created_at,public_metrics,referenced_tweets,entities,lang,attachments,author_id",
            "expansions": "attachments.media_keys,author_id",
            "media.fields": "url,preview_image_url,type,alt_text,width,height",
            "user.fields": "username,name",
        }
        try:
            logger.info("Searching recent watchlist + Grok posts")
            data = self._get("/tweets/search/recent", params=params)
        except Exception as e:
            logger.exception("Watchlist search failed: %s", e)
            return []

        tweets = data.get("data") or []
        includes = data.get("includes") or {}
        media_list = includes.get("media") or []
        media_by_key = {m["media_key"]: m for m in media_list if "media_key" in m}
        users = {u["id"]: u for u in (includes.get("users") or []) if "id" in u}

        results: list[dict[str, Any]] = []
        for tw in tweets:
            author_id = tw.get("author_id")
            username = (users.get(author_id) or {}).get("username") or "unknown"
            if is_high_signal(tw, author_username=username):
                results.append(self._item_from_tweet(tw, username, media_by_key))
        logger.info("  → %d watchlist hits after filter", len(results))
        return results

    def fetch_high_signal_posts(self) -> list[dict[str, Any]]:
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

                tweets, media_by_key = self.get_user_tweets(
                    user_id, max_results=POSTS_PER_ACCOUNT
                )
                logger.info(
                    "  → %d tweets returned by API for @%s", len(tweets), username
                )

                for tw in tweets:
                    if is_high_signal(tw, author_username=username):
                        results.append(self._item_from_tweet(tw, username, media_by_key))
                    else:
                        logger.debug(
                            "  filtered out: %s…", (tw.get("text") or "")[:60]
                        )

            except Exception as e:
                logger.exception("Failed to fetch @%s: %s", username, e)

        results.extend(self.search_watchlist())

        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for item in results:
            if item["id"] not in seen:
                seen.add(item["id"])
                unique.append(item)

        with_media = sum(1 for i in unique if i.get("media"))
        logger.info(
            "Total high-signal posts after filtering: %d (%d with media)",
            len(unique),
            with_media,
        )
        return unique

