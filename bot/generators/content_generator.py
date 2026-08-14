"""
Generate short X post + Markdown article from a high-signal source post
using the xAI / Grok API.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI

from config import XAI_API_KEY, XAI_BASE_URL, XAI_MODEL, ARTICLES_OUT, POSTS_OUT
from utils.logger import get_logger
from utils.filters import slugify

logger = get_logger("generator")

SYSTEM_PROMPT = """You are a precise news writer for Grokati, a focused site covering only Grok and xAI.

Core rules:
- Neutral, precise, and useful.
- Lead with the facts from the source post.
- Attribute every specific claim to the provided source.
- No hype, no speculation, no invented details.
- Slightly witty only when it genuinely helps clarity.

Limited context is allowed:
- You may briefly explain well-established public background (what Grok is, previous model names such as Grok 4 / 4.5 / 4.6, official product names like Grok Bot, Imagine, Grok Build, Voice mode, etc.).
- You may note that something is an official product from xAI when that is public knowledge.
- Do NOT invent performance numbers, release dates, pricing, feature lists, or future plans that are not in the source.
- Do NOT invent quotes or claim access to private information.

Length guidance:
- When the source is a real product/feature announcement, aim for 250–450 words of useful content.
- When the source is thin, keep the article short and honest rather than padding.

Output format (strict JSON only, no markdown fences, no extra text):
{
  "x_post": "A short, accurate post (1-3 sentences). Include the source link.",
  "title": "Clear, factual headline, max ~70 characters",
  "description": "One-sentence summary for SEO / cards, max ~160 characters",
  "body_markdown": "Full article body in Markdown. Use ## headings where helpful. End with clear attribution."
}
"""


class ContentGenerator:
    def __init__(self):
        if not XAI_API_KEY:
            raise ValueError("XAI_API_KEY is required")
        self.client = OpenAI(
            api_key=XAI_API_KEY,
            base_url=XAI_BASE_URL,
        )
        self.model = XAI_MODEL

    def _build_user_prompt(self, item: dict[str, Any]) -> str:
        return f"""Source post (primary material — do not invent beyond this):

Author: @{item['author']}
Date: {item.get('created_at', 'unknown')}
URL: {item['url']}

Text:
\"\"\"
{item['text']}
\"\"\"

Write an accurate short X post and a Markdown article based only on the above.

Requirements:
- If this is a real product/model/feature announcement, write a useful article (aim 250–450 words).
- You may add brief, well-established public context (what Grok is, previous model names, official product names).
- Do not invent numbers, dates, pricing, or features that are not in the source.
- Always include the source URL in both the X post and the article attribution.
"""

    def generate(self, item: dict[str, Any]) -> dict[str, Any] | None:
        """Call Grok API and return parsed {x_post, title, description, body_markdown}."""
        user_prompt = self._build_user_prompt(item)

        try:
            logger.info("Generating content for post %s …", item["id"])
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1800,
            )
            raw = response.choices[0].message.content or ""
            raw = raw.strip()

            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)

            data = json.loads(raw)

            required = ("x_post", "title", "description", "body_markdown")
            for key in required:
                if key not in data or not str(data[key]).strip():
                    logger.error("Missing or empty field in model response: %s", key)
                    return None

            # Reject very thin articles
            body = str(data["body_markdown"]).strip()
            word_count = len(body.split())
            if word_count < 100:
                logger.warning(
                    "Generated article too thin (%d words) — skipping post %s",
                    word_count,
                    item["id"],
                )
                return None

            return data

        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON from model: %s\nRaw: %s", e, raw[:400])
            return None
        except Exception as e:
            logger.exception("Generation failed for %s: %s", item["id"], e)
            return None

    def write_files(
        self,
        item: dict[str, Any],
        generated: dict[str, Any],
        live: bool = False,
        website_dir: Path | None = None,
    ) -> Path | None:
        title = generated["title"]
        slug = slugify(title)
        date_str = (item.get("created_at") or datetime.now(timezone.utc).isoformat())[:10]
        filename = f"{date_str}-{slug}.md"

        now = datetime.now(timezone.utc)
        pub_date = item.get("created_at") or now.isoformat()
        try:
            pub_date_short = pub_date[:10]
        except Exception:
            pub_date_short = now.strftime("%Y-%m-%d")

        source_name = f"@{item['author']} on X"
        source_url = item["url"]

        frontmatter = f"""---
title: "{title.replace('"', "'")}"
description: "{generated['description'].replace('"', "'")}"
pubDate: {pub_date_short}
source: "{source_name}"
sourceUrl: "{source_url}"
author: "Grokati"
draft: false
---

"""
        body = generated["body_markdown"].strip()
        if source_url not in body:
            body += f"\n\n*Source: [{source_name}]({source_url})*"

        full_md = frontmatter + body + "\n"

        out_path = ARTICLES_OUT / filename
        out_path.write_text(full_md, encoding="utf-8")
        logger.info("Wrote article → %s", out_path)

        post_path = POSTS_OUT / f"{date_str}-{slug}.txt"
        post_path.write_text(generated["x_post"].strip() + "\n", encoding="utf-8")
        logger.info("Wrote X post  → %s", post_path)

        if live and website_dir:
            website_dir.mkdir(parents=True, exist_ok=True)
            live_path = website_dir / filename
            live_path.write_text(full_md, encoding="utf-8")
            logger.info("LIVE: also wrote → %s", live_path)

        return out_path