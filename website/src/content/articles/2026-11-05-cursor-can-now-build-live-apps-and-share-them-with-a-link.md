---
title: "Cursor can now build live apps and share them with a link"
description: "Cursor announced that users can describe an app and have it built, set up with a database and auth, security-checked, and deployed to a shareable link. Available on all paid plans with cloud agents."
pubDate: 2026-11-05
source: "@cursor_ai on X"
sourceUrl: "https://x.com/cursor_ai/status/2118458629091426304"
author: "Grokati"
draft: false
category: "build"
hasVideo: true
---

On 5 November 2026, the official **@cursor_ai** account announced that users can now build live apps in Cursor and share them with a link.

> You can now build live apps in Cursor and share them with a link.
> 
> Agents have made it easier to write code, but most apps never make it off localhost. Describe the tool you want - Cursor will build it, set up a database, run deterministic and agentic security checks, and deploy.

A follow-up in the same thread said the capability is available now on all paid plans and pointed to the changelog.

## What was announced

From the @cursor_ai post and the linked changelog at cursor.com/changelog/build-live-apps:

* Describe the tool you want; Cursor builds the app, sets up a database, configures authentication, runs security checks, and deploys it.
* Available on all paid plans with cloud agents enabled. Update to the latest version of Cursor.
* Cursor scaffolds the web app, spins up a Postgres database if needed, sets up authentication behind Cursor SSO, and provisions hosting. If the app needs to connect to external systems, Cursor asks for the required secrets.
* When publishing, you pick a unique domain and receive a live link.
* On publish, Cursor runs deterministic and agentic security checks for issues such as secrets written in app files or exposed credentials. Nothing goes live until the checks pass and you explicitly publish.
* Share the app with specific people, groups, or your entire team, behind Cursor sign-in. On individual plans, apps can also be shared publicly.
* You can provision a Cursor API key so a script or Grok Bot can use the app.
* Supports deployment from new or existing repos on Cursor Origin and GitHub. Support for other providers such as GitLab is coming soon.

## Context

Cursor is included in The X Subscription alongside Grok, Grok Bot, and X Premium. Staff members @mattyp and @Baconbrix quoted the announcement in the context of using Grok Bot with the new capability.

The changelog notes examples of internal tools already being built at Cursor, such as ops tools, customer presentations, onboarding experiences, sales dashboards, and engineering portals.

## Limits of this report

This report covers only the statements in the 5 November 2026 @cursor_ai thread and the corresponding changelog page. It does not include pricing details beyond the plan requirement, full technical specifications of the security checks, exact rollout timing beyond “available now,” or independent verification of deployed apps. The video attached to the original post is not hosted here.

## Source

@cursor_ai on X: https://x.com/cursor_ai/status/2118458629091426304

Changelog: https://cursor.com/changelog/build-live-apps
