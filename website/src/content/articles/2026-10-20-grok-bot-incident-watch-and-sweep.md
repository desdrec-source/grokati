---
title: SpaceXAI uses Grok Bot teammates to detect and clear support incidents
description: Official post describes IncidentWatch spotting ticket spikes and IncidentSweep clearing approved batches, with a September example of 204 tickets in about 10 minutes.
pubDate: 2026-10-20
source: x.ai news
sourceUrl: https://x.ai/news/incident-sweep
author: Grokati
draft: false
category: bot
hasVideo: false
---

On 20 October 2026, SpaceXAI published **Using Grok Bot to detect and respond to incidents**.

> IncidentWatch spots ticket spikes before internal alerts fire. IncidentSweep clears the related backlog in an approved batch.

## What was announced

From the official news page by Chris Bowie and Isaac Hopkinson:

- Two specialised Grok Bot teammates for incidents: **IncidentWatch** and **IncidentSweep**.
- IncidentWatch reviews the previous 15 minutes of tickets every five minutes for spikes around the same problem. If the pattern does not match a known incident, it alerts the on-call support engineer with the apparent issue, matching ticket count, and examples.
- Support Bot (the primary customer-facing bot) can return to held matching tickets and respond once an incident is confirmed and posted to the status page.
- IncidentSweep finds matching tickets after resolution, reviews each, sets aside ones it cannot confidently connect, shows the proposed batch and exact message for engineer approval, then sends in small batches and records each action. It does not add tickets after approval.
- Example: during an incident on 18 September, IncidentSweep cleared 204 tickets in about 10 minutes with a support engineer reviewing and approving the batch.
- The post frames this as giving bots jobs (owning workflows) rather than individual tasks, building on the earlier customer-support case study.

## Context

This continues the September 22 post on rebuilding SpaceXAI and Cursor support around Grok Bot. That earlier piece already noted queue monitoring, automatic incident declaration at volume thresholds, and X sentiment checks. The 20 October post names the specific incident bots and their operating cadence.

## Limits of this report

The page does not specify which plan tiers can create similar bots, exact connector requirements, or how the September 18 incident was identified. Only statements on the news page are reported.

## Source

https://x.ai/news/incident-sweep
