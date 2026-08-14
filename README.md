# Grokati

**High-signal, accurate news about Grok and xAI.**  
Domain: [grokati.com](https://grokati.com)

> Accuracy and signal over volume. Never invent details. Always attribute sources. Prefer silence over low-value content.

Grokati is a Phase 1 MVP consisting of:

1. A clean static **Astro** website (Markdown content only)
2. A **Python** automation pipeline that monitors official X accounts and uses the Grok API to draft posts + articles (dry-run by default)

This is an independent, automated / AI-assisted project. It is **not** affiliated with xAI or X Corp.

---

## Quick Start (Website)

```bash
cd website
npm install
npm run dev
```

Open http://localhost:4321

To build for production (Vercel-ready):

```bash
npm run build
npm run preview
```

### Adding a new article manually

Drop a Markdown file with frontmatter into:

```
website/src/content/articles/your-slug.md
```

Required frontmatter:

```yaml
---
title: "Clear factual title"
description: "One-sentence summary"
pubDate: 2026-08-12
source: "xAI official announcement"
sourceUrl: "https://x.ai/news/..."
author: "Grokati"
draft: false
---
```

Then restart `npm run dev` or rebuild.

---

## Quick Start (Bot — Dry-run)

```bash
cd bot
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and add:
#   X_BEARER_TOKEN=...
#   XAI_API_KEY=...

python main.py
```

The bot will:

- Fetch recent posts from `@grok`, `@xai` (and filtered posts from `@elonmusk`)
- Apply strict high-signal filters
- Call the Grok API to generate a short X post + Markdown article
- Write everything under `bot/output/articles/` and `bot/output/posts/`

**Nothing is posted and the website content folder is not touched** while `LIVE_MODE=false` (the default).

### Enabling live mode (later)

In `bot/.env`:

```
LIVE_MODE=true
```

Generated Markdown files will also be copied into `website/src/content/articles/`.  
You still need to rebuild/deploy the Astro site yourself in Phase 1.

---

## Project Structure

```
grokati/
├── PLAN.md                 # Detailed Phase 1 plan
├── README.md               # This file
├── .gitignore
├── website/                # Astro site → deploy to Vercel
│   └── src/content/articles/   # Markdown only
└── bot/                    # Python pipeline
    ├── main.py
    ├── config.py
    ├── .env.example
    ├── monitors/
    ├── generators/
    ├── utils/
    └── output/             # Dry-run results land here
```

See `PLAN.md` for the full design decisions and scope.

---

## Writing Style (enforced in the LLM system prompt)

- Neutral, precise, useful
- Lead with the facts
- Attribute every claim
- No hype, no speculation, no invented details
- Slightly witty only when it helps clarity

---

## Required API Keys

| Service | Purpose | Where to get it |
|---------|---------|-----------------|
| X API Bearer Token | Read posts from official accounts | [developer.x.com](https://developer.x.com) |
| xAI API Key | Generate posts + articles with Grok | [console.x.ai](https://console.x.ai) |

The bot only needs **read** access to X in Phase 1.  
Posting to X is intentionally disabled until you explicitly enable live features later.

---

## Deploying the Website to Vercel (recommended path)

You already have Vercel. Follow these steps in order.

### 1. Put the code on GitHub

1. Create a new repository on GitHub (e.g. `grokati`). Make it public or private — your choice.
2. On your computer, open a terminal in the project folder and run:

```bash
cd path/to/grokati
git init
git add .
git commit -m "Initial Grokati Phase 1"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/grokati.git
git push -u origin main
```

(Replace `YOUR_USERNAME` with your GitHub username.)

### 2. Import the project in Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import the GitHub repository you just created.
3. **Important settings** (do not skip these):

| Setting              | Value                          |
|----------------------|--------------------------------|
| **Root Directory**   | `website`                      |
| Framework Preset     | Astro (auto-detected)          |
| Build Command        | `npm run build` (default)      |
| Output Directory     | `dist` (default)               |
| Install Command      | `npm install` (default)        |

4. Click **Deploy**.

Vercel will build the static site and give you a temporary URL like `grokati-xxxx.vercel.app`.

### 3. Connect your domain (grokati.com)

1. In the Vercel project → **Settings → Domains**
2. Add `grokati.com` and `www.grokati.com`
3. Follow the DNS instructions Vercel shows you (usually add an A record or CNAME at your domain registrar).

Once DNS propagates (can take a few minutes to a few hours), the site will be live at https://grokati.com.

### After the first deploy

- Every time you push a change to the `main` branch (especially new Markdown files in `website/src/content/articles/`), Vercel will automatically rebuild and update the live site.
- The bot stays separate for now. Keep using it in dry-run mode on your machine. When you like a generated article, copy the `.md` file into `website/src/content/articles/`, commit, and push.

---

## Phase 1 Limitations (by design)

- No database
- No images
- No newsletter / search / categories
- Dry-run only for the bot (safe default)
- Manual (or simple later) promotion of generated articles into the live site

These constraints keep the system simple, auditable, and easy to host.

---

## Next Steps After Phase 1

- GitHub Action or cron that runs the bot periodically
- Automatic copy of approved articles + Vercel deploy hook
- Optional live posting to an X account with rate-limit safety
- Better duplicate detection
- Simple OG images if desired

---

## License / Independence

This project is independent. All generated content must attribute original sources.  
Do not present Grokati as an official xAI channel.
