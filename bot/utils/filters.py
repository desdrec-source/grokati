"""
Strict high-signal filters for X posts.
Prefer silence over noise.
"""

from __future__ import annotations

import re
from typing import Any

from config import HIGH_SIGNAL_KEYWORDS


def is_reply(post: dict[str, Any]) -> bool:
    """True if the post is a reply."""
    ref = post.get("referenced_tweets") or []
    return any(r.get("type") == "replied_to" for r in ref)


def is_retweet(post: dict[str, Any]) -> bool:
    ref = post.get("referenced_tweets") or []
    return any(r.get("type") == "retweeted" for r in ref)


def contains_high_signal_keyword(text: str) -> bool:
    text_lower = text.lower()
    for kw in HIGH_SIGNAL_KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False


def is_high_signal(
    post: dict[str, Any],
    author_username: str | None = None,
    require_keyword_for_elon: bool = True,
) -> bool:
    """
    Decide whether a post is worth generating content from.

    Rules (Phase 1):
    - Skip pure replies and retweets (unless they contain substantial new text — keep simple for now).
    - Official accounts (@grok, @xai) are trusted more highly.
    - Elon posts are only kept if they clearly mention Grok / xAI related keywords.
    - Must not be empty or pure engagement bait (very short, only emojis, etc.).
    """
    text = (post.get("text") or "").strip()
    if not text or len(text) < 20:
        return False

    if is_retweet(post):
        return False

    # Allow replies only if they are substantial and from official accounts (rare)
    if is_reply(post) and author_username not in ("grok", "xai"):
        return False

    username = (author_username or "").lower().lstrip("@")

    if username in ("grok", "xai"):
        # Official accounts: accept most non-reply/non-rt content
        # Still skip pure "yes" / emoji-only style posts
        if len(text) < 40 and not contains_high_signal_keyword(text):
            return False
        return True

    if username == "elonmusk" or username == "elon":
        if require_keyword_for_elon:
            return contains_high_signal_keyword(text)
        return True

    # Fallback: keyword required
    return contains_high_signal_keyword(text)


def slugify(title: str) -> str:
    """Simple slug for filenames."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug[:80].strip("-")
