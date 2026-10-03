---
title: "SpaceXAI releases an experimental TypeScript SDK"
description: "On 2 October 2026, SpaceXAI staff released an experimental TypeScript SDK as @xai-official/sdk, covering text, voice, image, and video plus server-side tools. Interfaces may change before 1.0."
pubDate: 2026-10-02
source: "@ericzakariasson on X"
sourceUrl: "https://x.com/ericzakariasson/status/2106090512210088361"
author: "Grokati"
draft: false
category: "build"
hasVideo: true
---

On 2 October 2026, SpaceXAI staff member Eric Zakariasson posted that an experimental TypeScript SDK is out.

> we're releasing an experimental @SpaceXAI typescript sdk!
>
> npm install @xai-official/sdk
>
> get text, voice, image and video in one sdk, with the latest grok models
>
> and tools that run on our servers, like real-time X search, web search, code execution and remote mcp

A follow-up in the same thread said it is early and linked the repository and package: [github.com/xai-org/xai-sdk-ts](https://github.com/xai-org/xai-sdk-ts) and [npmjs.com/package/@xai-official/sdk](https://www.npmjs.com/package/@xai-official/sdk). @mattyp quoted the post: "we just launched a typescript sdk. the @SpaceXAI developer experience will be first class."

## What was announced

From the staff posts and the official repository README:

- Package name `@xai-official/sdk`, install with `npm install @xai-official/sdk` or `pnpm add @xai-official/sdk`
- Official TypeScript SDK for the SpaceXAI API, client class `SpaceXAI`, API key read from `XAI_API_KEY`
- Text, voice, image, and video in one SDK, with the latest Grok models
- Server-side tools named in the post: real-time X search, web search, code execution, and remote MCP
- README says the SDK has no runtime dependencies and covers the Responses API, image and video generation, the Files, Batch, and Voice APIs, tokenization, and model and account lookup
- Requirements listed in the README: Node.js 22.13 or later, a SpaceXAI API key, and an ESM project
- The README marks it experimental and says interfaces may change before 1.0

## Context

The repository is under the `xai-org` GitHub organization and is described there as the official TypeScript SDK. The quickstart example in the README calls `client.responses.create` with model `grok-4.7`. The SDK blocks browser and Worker use by default, because shipping a secret key to client-side code exposes it.

## Limits of this report

This report does not list every method, price, or rate limit. The README says the SDK is in early development and that interfaces may change between releases before 1.0. Version numbers beyond the install command were not stated in the announcement post.

## Source

[@ericzakariasson on X](https://x.com/ericzakariasson/status/2106090512210088361), 2 October 2026.

Repository: [xai-org/xai-sdk-ts](https://github.com/xai-org/xai-sdk-ts).
