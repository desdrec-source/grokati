---
title: Grok Bot 1.2.3 adds tool permissions and routine reconnect cards
description: The Grok Bot changelog for v1.2.3 (18 November 2026) adds per-tool permission settings, age restriction on signup, team admin controls on GitHub tools, and reconnect cards that also arrive as notifications and Slack/Teams messages.
pubDate: 2026-11-18
source: x.ai Grok Bot Changelog
sourceUrl: https://x.ai/changelog/bot
author: Grokati
draft: false
category: bot
hasVideo: false
---

Grok Bot version 1.2.3, dated 18 November 2026, adds connector tool permission controls and makes routine reconnect cards also appear as notifications and direct messages. The release also includes the changes from 1.2.1 and 1.2.2.

> Connector pages let you set each tool to Always allow, Auto-review, Needs approval, or Blocked. Requires Grok Bot 0.70.2 or later

## What was announced

From the Grok Bot changelog entry for v1.2.3:

**New**
- Connector pages let you set each tool to Always allow, Auto-review, Needs approval, or Blocked. Requires Grok Bot 0.70.2 or later.
- Clicking a message button in an MCP App puts its text in the chat box, ready for you to send.
- Signing up for Grok Bot requires you to be 18 or older.
- Team admins can limit which tools the built-in GitHub connector offers, and the Bot says when a team admin limited a tool. Teams

**Improved** (selected)
- When a routine needs you to reconnect an account, its reconnect card also arrives as a notification and as a Slack or Microsoft Teams direct message. Requires Grok Bot 0.79.2 or later.
- A routine that loses a connector sign-in skips its scheduled runs until you sign back in.
- Routines can read the earlier conversation in the chat they run in.
- For a site that has a connector, the Bot uses the connector, or shows its connect card, before opening the browser.
- The Bot keeps separate memories for people and organizations, your profile, your standing instructions, and your projects.

Additional improvements and fixes cover team MCP rules, flight booking behavior, memory handling, and various UI and reliability items. Full list is on the changelog.

## Context

The entry states that v1.2.3 also includes the changes from 1.2.1 and 1.2.2. Many of the new controls are marked as applying to Teams or Enterprise plans.

## Limits of this report

This report summarizes the public changelog text. It does not include rollout status, measured impact, or any details not written in the source.

## Source

- Grok Bot Changelog, v1.2.3, 18 November 2026: https://x.ai/changelog/bot
