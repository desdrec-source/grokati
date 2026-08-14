#!/usr/bin/env python3
"""Grokati automation entry point with processed-post memory."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    LIVE_MODE,
    WEBSITE_ARTICLES_DIR,
    ARTICLES_OUT,
    PROCESSED_PATH,
    validate_required,
)
from utils.logger import get_logger
from utils.state import ProcessedStore
from monitors.x_monitor import XMonitor
from generators.content_generator import ContentGenerator

logger = get_logger("main")


def main() -> int:
    logger.info("=== Grokati bot starting ===")
    logger.info("Mode: %s", "LIVE" if LIVE_MODE else "DRY-RUN (safe)")

    missing = validate_required()
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        return 1

    store = ProcessedStore(PROCESSED_PATH)
    seeded = 0
    seeded += store.seed_from_articles(WEBSITE_ARTICLES_DIR)
    seeded += store.seed_from_articles(ARTICLES_OUT)
    if seeded:
        logger.info("Processed memory now tracks %d posts", len(store.known_ids()))

    try:
        monitor = XMonitor()
        posts = monitor.fetch_high_signal_posts()
    except Exception as e:
        logger.exception("Failed to fetch posts: %s", e)
        return 1

    if not posts:
        logger.info("No high-signal posts found. Exiting quietly.")
        return 0

    new_posts = [p for p in posts if not store.has(p["id"])]
    skipped = len(posts) - len(new_posts)
    if skipped:
        logger.info("Skipping %d already-processed post(s)", skipped)
    if not new_posts:
        logger.info("Nothing new to process. Exiting quietly.")
        return 0

    try:
        generator = ContentGenerator()
    except Exception as e:
        logger.exception("Failed to initialize generator: %s", e)
        return 1

    success = 0
    for item in new_posts:
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
            store.mark(
                item["id"],
                url=item.get("url"),
                author=item.get("author"),
                title=generated.get("title"),
            )
            success += 1

    logger.info(
        "Done. Generated content for %d / %d new post(s) (%d already known).",
        success,
        len(new_posts),
        skipped,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())