---
title: "grok-voice-transcribe-1.0 reaches end of life"
description: "SpaceXAI docs dated 2 October 2026 say grok-voice-transcribe-1.0 is deprecated and at end of life. Requests to that slug are routed to grok-voice-transcribe-2.0 at the same price."
pubDate: 2026-10-02
source: "SpaceXAI docs release notes"
sourceUrl: "https://docs.x.ai/developers/release-notes"
author: "Grokati"
draft: false
category: "voice"
---

On 2 October 2026, SpaceXAI's developer release notes recorded the end of life for the first speech-to-text model slug.

> `grok-voice-transcribe-1.0` is deprecated and reaches end of life on October 2, 2026. All requests to that slug are routed to `grok-voice-transcribe-2.0` at the same price, with higher accuracy.

The note points to the Speech to Text docs.

## What was announced

From the 2 October release note:

- `grok-voice-transcribe-1.0` is deprecated and reached end of life on 2 October 2026
- Requests to that slug are routed to `grok-voice-transcribe-2.0`
- The routed requests stay at the same price
- SpaceXAI describes 2.0 as higher accuracy than 1.0

## Context

SpaceXAI announced Grok Voice Transcribe 2.0 on 17 September 2026. The 18 September news page said 2.0 would soon be the default in the Speech-to-Text API, and that 1.0 would be deprecated in the coming weeks. The same page said pricing stayed identical to 1.0: batch transcription at $0.10 per hour of audio and streaming at $0.20 per hour, with diarization, timestamps, and key terms included. The 17 September release note said the default was already `grok-voice-transcribe-2.0`, and that pinning `grok-voice-transcribe-1.0` would keep the older slug during the transition.

The 2 October note is the end of that transition. Pinning the 1.0 slug no longer selects the older model.

## Limits of this report

The release note does not say whether responses still label the model as 1.0, or how long the 1.0 slug will keep accepting traffic. Pricing figures above are from the 18 September announcement, not restated in the 2 October note, which only says the routed requests are at the same price.

## Source

[SpaceXAI docs release notes](https://docs.x.ai/developers/release-notes), October 2, 2026 entry.

Earlier announcement: [Introducing Grok Voice Transcribe 2.0](https://x.ai/news/grok-voice-transcribe-2).
