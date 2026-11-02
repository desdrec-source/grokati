---
title: grok-imagine-image-quality retired on the xAI API
description: Effective 2 November 2026, requests to the grok-imagine-image-quality slug are served by grok-imagine-image-2.0 at low quality.
pubDate: 2026-11-02
source: SpaceXSI Docs
sourceUrl: https://docs.x.ai/developers/migration/imagine-image-quality-nov-2
author: Grokati
draft: false
category: imagine
---

Effective 2 November 2026, the `grok-imagine-image-quality` model slug is retired from the xAI API. Requests continue to resolve but are served by `grok-imagine-image-2.0` with quality set to low.

> `grok-imagine-image-2.0` now covers everything `grok-imagine-image-quality` was used for, at a lower price. Effective November 2, 2026, the `grok-imagine-image-quality` model slug is retired from the xAI API. Its 60-day notice period began on September 2, 2026.

## What was announced

From the SpaceXSI migration guide:

- Starting 2 November 2026, requests to `grok-imagine-image-quality` on `/v1/images/generations` and `/v1/images/edits` are served by **grok-imagine-image-2.0 with quality: "low"**.
- The request and response shapes are unchanged. The model field on responses reports the model that served the request.
- Requests to `grok-imagine-image-pro` (which already redirected to `grok-imagine-image-quality`) follow through to `grok-imagine-image-2.0` at low.
- `grok-imagine-image` (1.0) is not affected.
- `grok-imagine-image-2.0` at low quality is $0.01 per image cheaper than `grok-imagine-image-quality` at every resolution. Continued use of the retired slug is billed at the low rate.
- Recommended replacement is to switch explicitly to `grok-imagine-image-2.0` so quality can be chosen (`low`, `medium`, or `auto`). Auto currently uses low for generation and medium for editing.

## Context

The 60-day notice period began on 2 September 2026, as noted in the September release notes and the migration guide (last updated 2 September 2026). The slug continues to resolve after the retirement date, avoiding immediate breakage for existing code.

## Limits of this report

This brief reports only the statements on the official migration page. It does not include independent verification of pricing tables, Arena rankings, or the exact quality of the low setting relative to the retired model. No staff post on X announcing the effective date was found in the search window.

## Source

[SpaceXSI Docs: grok-imagine-image-quality Retirement on November 2, 2026](https://docs.x.ai/developers/migration/imagine-image-quality-nov-2)
