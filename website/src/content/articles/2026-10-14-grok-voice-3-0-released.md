---
title: Introducing Grok Voice 3.0
description: SpaceXSI announced Grok Voice 3.0, the world’s most intelligent speech-to-speech model, ranking #1 on the Artificial Analysis Speech-to-Speech Index and available today in the Voice Agent API at the same price as Grok Voice 2.0.
pubDate: 2026-10-14
source: x.ai news
sourceUrl: https://x.ai/news/grok-voice-3
author: Grokati
draft: false
category: voice
featured: true
---

SpaceXSI announced Grok Voice 3.0 on 14 October 2026.

> Today, we’re announcing Grok Voice 3.0, the world’s most intelligent speech-to-speech model. It sets a new record for resolving customer support calls, has class-leading latency at under one second, and costs less than other frontier models. Grok Voice powers millions of conversations a day across Tesla and SpaceX, and is available today in the API at the same price as its predecessor.

## What was announced

- Grok Voice 3.0 is a speech-to-speech model available today in the Voice Agent API.
- Pricing is $0.08 per minute ($4.80 per hour), unchanged from Grok Voice 2.0.
- Agents using `grok-voice-latest` have been switched over automatically.
- In Artificial Analysis testing dated 13 October 2026, it ranks #1 on the Speech-to-Speech Index at 86.9 (versus 81.3 for Grok Voice 2.0, 83.2 for GPT-Live-1 Astra Medium, and 82.6 for Gemini 3.8 Live Extended Thinking High).
- It scores 98.5% on Speech Reasoning (Big Bench Audio), 1070 Elo on Human Preference (Speech Agent Arena), 94.8% on Task Completion (Task Success Rate), and 97.0% on Conversational Dynamics (Full Duplex Bench).
- On τ-Voice it scores 71.6%, comparable with GPT-Live-1 (Astra) but at 40% lower latency.
- On ServiceNow’s EVA-Bench it achieves the highest accuracy score at 74% and is described as the best-performing model when jointly scored across accuracy and customer experience.
- It handles millions of conversations a day in Tesla vehicles (including Connectors and Grok Bot tasks) and powers Grok Bot’s voice mode.
- Starlink call centers use Grok Voice to answer 20,000 customer calls every day across multiple languages; roughly 70% are resolved with no human in the loop, and one in four sales calls ends in a purchase before the caller hangs up.

## Context

Grok Voice is the speech-to-speech system used in Tesla vehicles and Starlink support. Grok Voice 2.0 was the previous release; docs note that `grok-voice-2.0` is now deprecated in favor of `grok-voice-3.0` or `grok-voice-latest` at the same price.

## Limits of this report

This article reports only statements in the 14 October 2026 x.ai news post and the linked official @SpaceXSI post on X. It does not include independent re-testing of benchmarks, exact latency measurements beyond the stated “under one second” and “40% lower latency,” availability outside the API, or any features not named in the source.

## Source

https://x.ai/news/grok-voice-3

https://x.com/SpaceXSI/status/2110416580899168305
