---
title: "Memory in Grok Build"
description: "xAI announced cross-session memory for Grok Build: background notes on conventions, decisions and project facts that later sessions read back."
pubDate: 2026-09-16
source: "x.ai"
sourceUrl: "https://x.ai/news/grok-build-memory"
author: "Grokati"
draft: false
category: "build"
featured: true
hasVideo: false
---

On 16 September 2026, SpaceXAI published an official news post introducing memory for Grok Build.

> Grok Build now carries conventions, decisions, and project facts from one session to the next. Notes are written in the background as you work and read back when you return to the project.

## What was announced

From the x.ai news post:

- After a turn completes, Grok reviews it in the background and records durable items: conventions, decisions, and project facts. Capture does not interrupt the session.
- Notes are stored as markdown files, one topic per subject. Each project has its own workspace scope; a global scope holds preferences that apply everywhere.
- Before starting related work, Grok reads the relevant topics. Instructions in the current conversation take precedence over stored notes.
- New commands: `/memory` opens a read-only browser of memory files; `/dream` organises recent notes into topic files (and also runs periodically in the background).
- Memory is available now and applies to new sessions: run `/new` or start a fresh `grok` session; notes begin after the first completed turn.

The post states that task state, tentative conclusions, secrets, and material already covered by the repository or its docs are left out of memory.

## Context

Grok Build is SpaceXAI’s coding agent and terminal harness. The memory feature is presented as a way for the agent to retain project-specific knowledge across sessions without the user re-explaining conventions or decisions each time.

## Limits of this report

This article reports only the statements in the official x.ai news post. It does not include independent testing of capture quality, storage location details beyond what was stated, plan gating, or comparisons to other tools.

## Source

[Memory in Grok Build](https://x.ai/news/grok-build-memory) — SpaceXAI, 16 September 2026.
