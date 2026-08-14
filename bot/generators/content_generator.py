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

SYSTEM_PROMPT = """You are a precise news writer for Grokati, a high-signal site covering only Grok and xAI.

Core rules (never break these):
- Neutral, precise, and useful.
- Lead with the facts.
- Attribute every claim to the provided source.
- No hype, no speculation, no invented details, no filler.
- Slightly witty only when it genuinely helps clarity.
- Prefer silence: if the source is thin, write a short accurate piece rather than padding.
- Never claim access to private information or future plans that are not in the source.

Output format (strict):
You must reply with valid JSON only, no markdown fences, no extra text:
{
  "x_post": "A short, accurate post (1-4 sentences or a short thread of 2-3 posts separated by \\n\\n---\\n\\n). Ready to publish on X. Include the source link.",
  "title": "Clear, factual headline, max ~70 characters",
  "description": "One-sentence summary for SEO / cards, max ~160 characters",
  "body_markdown": "The full article body in Markdown (300-500 words preferred, shorter if source is thin). Use ## headings where helpful. End with a short attribution line."
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
If the post is an official product/model announcement, focus on what was stated.
Always keep the source URL in the X post and in the article attribution.
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

            # Strip accidental markdown fences if the model adds them
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)

            data = json.loads(raw)

            required = ("x_post", "title", "description", "body_markdown")
            for key in required:
                if key not in data or not str(data[key]).strip():
                    logger.error("Missing or empty field in model response: %s", key)
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
        """
        Write the Markdown article and the X post text to the output folders.
        Returns path to the written Markdown file.
        """
        title = generated["title"]
        slug = slugify(title)
        # Make filename unique-ish with date + short id
        date_str = (item.get("created_at") or datetime.now(timezone.utc).isoformat())[:10]
        filename = f"{date_str}-{slug}.md"

        # Frontmatter
        now = datetime.now(timezone.utc)
        pub_date = item.get("created_at") or now.isoformat()
        # Normalize to YYYY-MM-DD for frontmatter
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
        # Ensure attribution is present
        if source_url not in body:
            body += f"\n\n*Source: [{source_name}]({source_url})*"

        full_md = frontmatter + body + "\n"

        # Write dry-run / output copy
        out_path = ARTICLES_OUT / filename
        out_path.write_text(full_md, encoding="utf-8")
        logger.info("Wrote article → %s", out_path)

        # Write X post text
        post_path = POSTS_OUT / f"{date_str}-{slug}.txt"
        post_path.write_text(generated["x_post"].strip() + "\n", encoding="utf-8")
        logger.info("Wrote X post  → %s", post_path)

        # Optional live copy into the Astro content folder
        if live and website_dir:
            website_dir.mkdir(parents=True, exist_ok=True)
            live_path = website_dir / filename
            live_path.write_text(full_md, encoding="utf-8")
            logger.info("LIVE: also wrote → %s", live_path)

        return out_path
