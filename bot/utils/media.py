"""Download source-post media for article images, with quality filters."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

from utils.logger import get_logger

logger = get_logger("media")

MIN_WIDTH = 400
MIN_HEIGHT = 200
MIN_BYTES = 12_000
MAX_BYTES = 8_000_000
MIN_MEAN_BRIGHTNESS = 18


def _extension_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def _is_usable_candidate(m: dict[str, Any]) -> bool:
    mtype = (m.get("type") or "").lower()
    if mtype and mtype != "photo":
        logger.info("Skipping non-photo media (type=%s)", mtype)
        return False
    if not m.get("url"):
        return False
    w = m.get("width") or 0
    h = m.get("height") or 0
    if w and h and (w < MIN_WIDTH or h < MIN_HEIGHT):
        logger.info("Skipping tiny media %sx%s", w, h)
        return False
    return True


def _mean_brightness(data: bytes) -> float | None:
    try:
        from PIL import Image
        import statistics

        img = Image.open(BytesIO(data))
        img = img.convert("RGB")
        img.thumbnail((160, 160))
        pixels = list(img.getdata())
        if not pixels:
            return None
        vals = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in pixels]
        return float(statistics.fmean(vals))
    except Exception as e:
        logger.debug("Brightness check skipped: %s", e)
        return None


def download_source_image(
    media_list: list[dict[str, Any]],
    dest_dir: Path,
    basename: str,
) -> tuple[Path, str] | None:
    if not media_list:
        return None

    dest_dir.mkdir(parents=True, exist_ok=True)
    candidates = [m for m in media_list if _is_usable_candidate(m)]
    if not candidates:
        logger.info("No usable source media after filters")
        return None

    for media in candidates:
        url = media["url"]
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
            data = resp.content
            size = len(data)

            if size < MIN_BYTES:
                logger.info("Skipping small download (%d bytes)", size)
                continue
            if size > MAX_BYTES:
                logger.info("Skipping oversized download (%d bytes)", size)
                continue

            brightness = _mean_brightness(data)
            if brightness is not None and brightness < MIN_MEAN_BRIGHTNESS:
                logger.info(
                    "Skipping near-black media (mean brightness %.1f)", brightness
                )
                continue

            content_type = (resp.headers.get("content-type") or "").lower()
            if "png" in content_type:
                dest = dest_dir / f"{basename}.png"
            elif "webp" in content_type:
                dest = dest_dir / f"{basename}.webp"
            elif "gif" in content_type:
                dest = dest_dir / f"{basename}.gif"

            dest.write_bytes(data)
            alt = (media.get("alt") or "").strip() or "Image from the source post"
            logger.info("Saved source image (%d bytes) → %s", size, dest)
            return dest, alt
        except Exception as e:
            logger.warning("Failed to download media from %s: %s", url[:80], e)
            continue

    logger.info("All media candidates failed quality checks")
    return None