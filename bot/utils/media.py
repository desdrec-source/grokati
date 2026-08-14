"""Download source-post media for article images."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

from utils.logger import get_logger

logger = get_logger("media")


def _extension_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def download_source_image(
    media_list: list[dict[str, Any]],
    dest_dir: Path,
    basename: str,
) -> tuple[Path, str] | None:
    if not media_list:
        return None

    dest_dir.mkdir(parents=True, exist_ok=True)
    first = media_list[0]
    url = first.get("url")
    if not url:
        return None

    ext = _extension_from_url(url)
    dest = dest_dir / f"{basename}{ext}"

    try:
        logger.info("Downloading source media → %s", dest.name)
        resp = requests.get(
            url,
            timeout=45,
            headers={"User-Agent": "GrokatiBot/0.1"},
        )
        resp.raise_for_status()
        content_type = (resp.headers.get("content-type") or "").lower()
        if "png" in content_type:
            dest = dest_dir / f"{basename}.png"
        elif "webp" in content_type:
            dest = dest_dir / f"{basename}.webp"
        elif "gif" in content_type:
            dest = dest_dir / f"{basename}.gif"

        dest.write_bytes(resp.content)
        alt = (first.get("alt") or "").strip() or "Image from the source post"
        logger.info("Saved source image (%d bytes) → %s", len(resp.content), dest)
        return dest, alt
    except Exception as e:
        logger.warning("Failed to download media from %s: %s", url[:80], e)
        return None