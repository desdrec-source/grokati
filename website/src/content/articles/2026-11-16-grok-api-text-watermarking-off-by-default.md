---
title: Grok API text watermarking is off by default
description: SpaceXSI docs now state text watermarking is off by default. Team admins can turn it on per model. Elon Musk confirmed watermarking is only on where required by law or requested by the user.
pubDate: 2026-11-16
source: docs.x.ai and @elonmusk on X
sourceUrl: https://docs.x.ai/developers/advanced-api-usage/watermarking.md
author: Grokati
draft: false
category: models
hasVideo: false
---

SpaceXSI documentation now states that text watermarking on the Grok API is off by default. Team admins can enable it per model in the Console. Elon Musk confirmed the policy on X.

> Text watermarking is off by default. Team admins can turn it on per model in the SpaceXSI Console's team settings.

## What was announced

From the current SpaceXSI Output Watermarking docs:

- Text watermarking is off by default.
- Team admins can turn it on per model in the SpaceXSI Console team settings.
- The setting applies to every API key on the team.
- Changes apply to new requests within 5 minutes.
- Covered models include grok-4.7, grok-4.6, grok-4.5, grok-4.3, and the grok-4.20 variants.
- Responses include an `x-watermark` header when the watermark was applied.
- The watermark is invisible and applied during generation by slightly shaping token selection. It adds no characters or markup.

On 14 November 2026, Elon Musk posted on X:

> Text watermarking with Grok is only on where required by law or requested by the user

## Context

Earlier docs and a Grokati report from 7 November stated that text watermarking would be on by default from that date, with an opt-out available to team admins. The current docs reverse the default to off.

## Limits of this report

This report covers only the statements in the current docs and Elon Musk's post. It does not include the timing of the docs update, any customer emails, or implementation details beyond what is written in the source.

## Source

- SpaceXSI Output Watermarking docs: https://docs.x.ai/developers/advanced-api-usage/watermarking.md
- Elon Musk on X, 14 November 2026: https://x.com/elonmusk/status/2121644169462681818
