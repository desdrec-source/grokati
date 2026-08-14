#!/usr/bin/env python3
"""
Grokati automation entry point.

Default behaviour = dry-run:
  - Fetches high-signal posts from official accounts
  - Generates X post text + Markdown article via Grok API
  - Writes files only under bot/output/
  - Does NOT post to X and does NOT modify the website content folder

Set LIVE_MODE=true in .env to also copy generated Markdown into the Astro articles folder.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make sure bot/ is on the path when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    LIVE_MODE,
    WEBSITE_ARTICLES_DIR,
    validate_required,
)
from utils.logger import get_logger
from monitors.x_monitor import XMonitor
from generators.content_generator import ContentGenerator

logger = get_logger("main")


def main() -> int:
    logger.info("=== Grokati bot starting ===")
    logger.info("Mode: %s", "LIVE" if LIVE_MODE else "DRY-RUN (safe)")

    missing = validate_required()
    if missing:
        logger.error(
            "Missing required environment variables: %s",
            ", ".join(missing),
        )
        logger.error("Copy .env.example → .env and fill in the keys.")
        return 1

    # 1. Fetch high-signal posts
    try:
        monitor = XMonitor()
        posts = monitor.fetch_high_signal_posts()
    except Exception as e:
        logger.exception("Failed to fetch posts: %s", e)
        return 1

    if not posts:
        logger.info("No high-signal posts found. Exiting quietly (this is expected sometimes).")
        return 0

    # 2. Generate content for each
    try:
        generator = ContentGenerator()
    except Exception as e:
        logger.exception("Failed to initialize generator: %s", e)
        return 1

    success = 0
    for item in posts:
        logger.info("Processing @%s — %s", item["author"], item["id"])
        generated = generator.generate(item)
        if not generated:
            logger.warning("Skipping post %s (generation failed)", item["id"])
            continue

        path = generator.write_files(
            item,
            generated,
            live=LIVE_MODE,
            website_dir=WEBSITE_ARTICLES_DIR if LIVE_MODE else None,
        )
        if path:
            success += 1

    logger.info("Done. Generated content for %d / %d posts.", success, len(posts))
    if not LIVE_MODE:
        logger.info(
            "Dry-run complete. Inspect bot/output/articles/ and bot/output/posts/."
        )
        logger.info("To enable live writing into the website, set LIVE_MODE=true.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
