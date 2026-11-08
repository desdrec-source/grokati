---
title: Grok API text watermarking is on by default from 7 November
description: SpaceXSI docs say text from seven Grok models includes an invisible watermark by default starting 7 November 2026, with team admin opt-out.
pubDate: 2026-11-07
source: SpaceXSI Docs
sourceUrl: https://docs.x.ai/developers/advanced-api-usage/watermarking.md
author: Grokati
draft: false
category: models
hasVideo: false
---

Starting 7 November 2026, text responses from seven Grok API models include an invisible watermark by default.

> Starting November 7, 2026, responses from these models include a watermark. It's on by default, and you can opt out per model.

## What was announced

From the SpaceXSI Output Watermarking docs:

* Watermarking applies to text output from these models: grok-4.7, grok-4.6, grok-4.5, grok-4.3, grok-4.20-reasoning, grok-4.20-non-reasoning, and grok-4.20-multi-agent.
* It covers the Responses API and the Chat Completions API on every SpaceXSI endpoint, including the global https://api.x.ai and regional endpoints.
* It applies to ordinary text responses, structured outputs, and tool call arguments.
* There is no request parameter. The response format is unchanged apart from an `x-watermark` header. `x-watermark: true` means the output for that request was generated with the watermark.
* The watermark is not visible. It is applied while the model generates text by slightly shaping which tokens the model picks. It adds no characters, markup, or hidden text.
* Detection is statistical. Longer text gives a stronger signal. Access to watermark detection is granted by application.
* Team admins can opt out per model in the SpaceXSI Console. The setting applies to every API key on the team. Changes apply to new requests within 5 minutes. Opting out requires confirming that an exception under applicable law applies.
* Some models may be locked on for a team. Opt-ins and opt-outs are recorded in the team audit log.
* Watermarking does not change response quality or speed.

## Context

The docs state that SpaceXSI watermarks text model output to comply with the EU AI Act. The page is under Advanced API Usage.

## Limits of this report

This report covers only the claims in the Output Watermarking documentation. It does not include consumer Grok app, website, or X subscription behaviour, detection API access details beyond the application form, or any performance measurements.

## Source

SpaceXSI Docs, Output Watermarking. https://docs.x.ai/developers/advanced-api-usage/watermarking.md
