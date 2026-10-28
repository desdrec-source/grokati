---
title: xAI API adds custom moderation controls for text requests
description: Developers can now pass a guidelines array to set how Grok handles nsfw, violence, and profanity categories on Chat Completions and Responses API requests.
pubDate: 2026-10-27
source: docs.x.ai
sourceUrl: https://docs.x.ai/developers/release-notes
author: Grokati
draft: false
category: models
---

On 27 October 2026, the SpaceXSI docs release notes listed a new API capability.

> You can now set content guidelines on text API requests. Add a `guidelines` array to a Chat Completions or Responses API request to set how Grok handles content in the `nsfw`, `violence`, and `profanity` categories. Grok follows the guidelines as it writes its response.

## What was announced

From the release notes:

* A `guidelines` array can be added to Chat Completions or Responses API requests.
* The array sets how Grok handles content in the `nsfw`, `violence`, and `profanity` categories.
* Grok follows the guidelines as it writes its response.
* Documentation is linked at Custom Moderation Controls.

## Context

This is an incremental API control for developers using Grok text models. It follows earlier release notes on models such as Grok 4.7 and voice endpoints.

## Limits of this report

The release notes do not describe the exact schema of the guidelines array, default behaviour, which models support it, rate limits, or examples. Only the wording in the release notes is reported.

## Source

https://docs.x.ai/developers/release-notes
