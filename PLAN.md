# Grokati — Phase 1 Detailed Plan

**Project:** Grokati  
**Domain:** grokati.com  
**Goal:** High-signal, accurate news site + automated pipeline focused exclusively on Grok and xAI updates.  
**Core principle:** Accuracy and signal over volume. Never invent details. Always attribute sources. Prefer silence over low-value content.

## Phase 1 MVP Scope (Locked)

### What is included
- Static Astro website (Markdown content only)
- Homepage with latest articles (card/grid)
- Individual article pages
- About page (explicitly states automated / AI-assisted nature)
- Basic RSS feed
- SEO basics (title, description, Open Graph)
- Python automation pipeline in **dry-run mode** (default)
- Monitoring of official X accounts + limited high-signal keywords
- Grok API generation of:
  1. Short accurate X post/thread
  2. Markdown article (frontmatter + ~300–500 words)
- Clear attribution of every source
- Config via `.env`
- Logging + error handling
- Beginner-friendly README + `.env.example`

### Explicitly out of scope for Phase 1
- Database
- Images / media uploads
- Newsletter
- Search
- Categories / tags UI
- Live posting to X (dry-run only)
- Automatic deploy / Git push (manual or simple later)
- Comments, user accounts, analytics beyond basic

## Project Structure

```
grokati/
├── PLAN.md                 # This file
├── README.md               # Main documentation & setup
├── .gitignore
├── website/                # Astro static site (Vercel target)
│   ├── package.json
│   ├── astro.config.mjs
│   ├── tsconfig.json
│   ├── public/
│   │   └── favicon.svg
│   └── src/
│       ├── content/
│       │   ├── config.ts           # Content collection schema
│       │   └── articles/           # Markdown files only
│       │       ├── *.md
│       ├── components/
│       │   ├── Header.astro
│       │   ├── Footer.astro
│       │   └── ArticleCard.astro
│       ├── layouts/
│       │   ├── BaseLayout.astro
│       │   └── ArticleLayout.astro
│       ├── pages/
│       │   ├── index.astro
│       │   ├── about.astro
│       │   ├── articles/
│       │   │   └── [slug].astro
│       │   └── rss.xml.ts
│       └── styles/
│           └── global.css
└── bot/                    # Python automation (separate)
    ├── requirements.txt
    ├── .env.example
    ├── config.py
    ├── main.py                 # Entry point (dry-run by default)
    ├── monitors/
    │   └── x_monitor.py
    ├── generators/
    │   └── content_generator.py
    ├── utils/
    │   ├── logger.py
    │   └── filters.py
    └── output/                 # Dry-run generated files land here
        ├── articles/           # Ready-to-copy Markdown
        └── posts/              # Generated X post text
```

## Website Design Decisions

- **Dark mode by default**, clean modern typography, mobile-first.
- No heavy JS frameworks. Pure Astro + minimal CSS.
- Content collections for type-safe Markdown articles.
- Frontmatter required fields: `title`, `description`, `pubDate`, `source`, `sourceUrl`, `author` (always "Grokati"), optional `draft`.
- Homepage sorts by `pubDate` descending, shows cards.
- Article pages use a simple readable layout with clear source attribution at top and bottom.
- RSS via `@astrojs/rss`.
- SEO: every page has proper `<title>`, meta description, Open Graph tags.

## Automation Pipeline Design

### High-level flow (dry-run)
1. Load config from `.env` + `config.py`
2. Fetch recent posts from:
   - Official accounts: `@grok`, `@xai` (and optionally `@elonmusk` filtered for Grok/xAI keywords)
   - Limited keyword search (model release, announcement, API, etc.)
3. Apply strict filters:
   - Must be high-signal (official or clear announcement)
   - Skip replies, pure engagement bait, speculation, duplicates
   - Deduplicate against already-generated articles (simple title/slug or source ID check)
4. For each selected item:
   - Call Grok API with carefully engineered system prompt (neutral, precise, attribute everything, no invention)
   - Generate:
     a. Short X post / thread text
     b. Full Markdown article with correct frontmatter
5. Write files to `bot/output/articles/` and `bot/output/posts/`
6. Log everything clearly. Never post or push in dry-run.
7. Exit cleanly.

### Live mode (future toggle)
- Set `LIVE_MODE=true` in `.env`
- Will additionally:
  - Copy/generated Markdown into `website/src/content/articles/`
  - (Optional later) post to X via API
  - (Optional later) trigger Vercel deploy or Git commit

### Writing style system prompt (to be embedded)
- Neutral, precise, useful
- Lead with the facts
- Attribute every claim to the original source
- No hype, no speculation, no invented details
- Slightly witty only when it helps clarity
- Always include source link and clear “This article is based on …” attribution

## Sample Content Strategy
Create 2–3 high-quality sample Markdown articles based on real recent official announcements (Grok 4.6 release, Grok Bot, etc.) so the site looks complete and realistic from day one.

## Development Order
1. ✅ Create clean folder structure
2. ✅ Write this detailed plan
3. Build Astro website skeleton + styling + sample articles
4. Build Python bot (dry-run) with good structure, logging, config
5. Write comprehensive README + `.env.example`
6. Verify everything works locally (Astro build, bot dry-run)

## Success Criteria for Phase 1
- `cd website && npm install && npm run build` succeeds
- Homepage, article pages, About, RSS all work
- Sample articles render correctly with attribution
- `cd bot && python main.py` runs in dry-run, produces valid Markdown + post text without errors
- Documentation is clear enough for a beginner to follow
- Zero invented facts in samples or generated style

## Later Phases (not now)
- GitHub Action or cron for the bot
- Automatic copy of generated articles + Vercel deploy hook
- Live X posting with rate-limit safety
- Simple image support / OG images
- Better filtering / embedding similarity for duplicates
- Categories or topic pages if volume justifies

---

This plan prioritizes simplicity, accuracy, and maintainability so the project can ship quickly and improve safely.
