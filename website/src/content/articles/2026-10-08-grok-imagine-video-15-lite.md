---
title: "Grok Imagine Video 1.5 Lite is live in the API"
description: "On 8 October 2026, @imagine said Video 1.5 Lite is live in the Grok Imagine API for text-to-video and image-to-video, with per-second prices at 480p, 720p, and 1080p."
pubDate: 2026-10-08
source: "@imagine on X"
sourceUrl: "https://x.com/imagine/status/2108280250673352929"
author: "Grokati"
draft: false
category: "imagine"
hasVideo: true
---

On 8 October 2026, the official Grok Imagine account said Video 1.5 Lite is live in the Grok Imagine API.

> Video 1.5 Lite is live in the Grok Imagine API. The new workhorse for text-to-video and image-to-video.
>
> $0.02/sec at 480p
> $0.03/sec at 720p
> $0.14/sec at 1080p

Elon Musk replied to that post: “Automatically used by Grok @Bot.”

## What was announced

From the @imagine post:

- Video 1.5 Lite is live in the Grok Imagine API.
- The account calls it the workhorse for text-to-video and image-to-video.
- Stated prices are $0.02 per second at 480p, $0.03 per second at 720p, and $0.14 per second at 1080p.
- The post includes a video. This page does not host that file.

SpaceXAI docs, last updated 8 October 2026, name the model `grok-imagine-video-1.5-lite`. The video overview says it does text-to-video and image-to-video with lip-synced speech, clips of 1–15 seconds, and 1080p by upscaling 720p. The same page lists the same per-second prices. It recommends the lite model for simple videos, and `grok-imagine-video-1.5` when references, voices, pinned frames, or native 1080p are needed. The lite column in that table does not list reference images, voice references, or keyframes.

## Context

The docs page compares lite with `grok-imagine-video-1.5`, which it describes as native 1080p text-to-video and image-to-video, up to 14 reference images, up to 3 voice references, and pinned frames, at $0.08 / $0.14 / $0.25 per second for 480p / 720p / 1080p. Elon Musk’s reply says the lite model is automatically used by Grok Bot. The reply does not say when that routing started or whether users can choose the model.

## Limits of this report

The @imagine post does not name rate limits, regions, or a consumer-app rollout. Docs list regions us-east-1 and us-west-2 and a 10 requests-per-second limit on the model page; this report does not add claims beyond those pages. Only the statements in the source post, the Musk reply, and the cited docs are reported.

## Source

[@imagine on X](https://x.com/imagine/status/2108280250673352929), 8 October 2026. Reply from [@elonmusk](https://x.com/elonmusk/status/2108294618597216470). Docs: [Video overview](https://docs.x.ai/developers/model-capabilities/video/overview) and [grok-imagine-video-1.5-lite](https://docs.x.ai/developers/models/grok-imagine-video-1.5-lite).
