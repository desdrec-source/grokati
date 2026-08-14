"""
Grokati bot configuration.
Loads from environment variables (see .env.example).
"""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the bot directory
BOT_DIR = Path(__file__).resolve().parent
load_dotenv(BOT_DIR / ".env")

# --- Mode ---
LIVE_MODE: bool = os.getenv("LIVE_MODE", "false").lower() in ("1", "true", "yes")

# --- X API ---
X_BEARER_TOKEN: str | None = os.getenv("X_BEARER_TOKEN")
X_API_KEY: str | None = os.getenv("X_API_KEY")
X_API_SECRET: str | None = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN: str | None = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET: str | None = os.getenv("X_ACCESS_TOKEN_SECRET")

# --- xAI / Grok ---
XAI_API_KEY: str | None = os.getenv("XAI_API_KEY")
XAI_BASE_URL: str = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
XAI_MODEL: str = os.getenv("XAI_MODEL", "grok-4-latest")

# --- Monitoring ---
WATCH_ACCOUNTS: list[str] = [
    a.strip().lstrip("@")
    for a in os.getenv("WATCH_ACCOUNTS", "grok,xai").split(",")
    if a.strip()
]
WATCH_ELON: bool = os.getenv("WATCH_ELON", "true").lower() in ("1", "true", "yes")
HIGH_SIGNAL_KEYWORDS: list[str] = [
    k.strip()
    for k in os.getenv(
        "HIGH_SIGNAL_KEYWORDS",
        "Grok 4,Grok-4,Grok 4.,model release,API update,announcement,Grok Bot,Grok Build,xAI",
    ).split(",")
    if k.strip()
]
POSTS_PER_ACCOUNT: int = int(os.getenv("POSTS_PER_ACCOUNT", "15"))

# --- Paths ---
OUTPUT_DIR: Path = BOT_DIR / os.getenv("OUTPUT_DIR", "output")
ARTICLES_OUT: Path = OUTPUT_DIR / "articles"
POSTS_OUT: Path = OUTPUT_DIR / "posts"
WEBSITE_ARTICLES_DIR: Path = (
    BOT_DIR / os.getenv("WEBSITE_ARTICLES_DIR", "../website/src/content/articles")
).resolve()

# --- Logging ---
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

# Ensure output directories exist
ARTICLES_OUT.mkdir(parents=True, exist_ok=True)
POSTS_OUT.mkdir(parents=True, exist_ok=True)


def validate_required() -> list[str]:
    """Return list of missing critical keys for a basic dry-run."""
    missing = []
    if not X_BEARER_TOKEN:
        missing.append("X_BEARER_TOKEN")
    if not XAI_API_KEY:
        missing.append("XAI_API_KEY")
    return missing
