---
title: Retro QA Practices Lead to QA Testing Flaws
date: 2018-11-14
author: Eric Chapman
slug: retro-qa-practices-lead-to-qa-testing-flaws
category: quality-engineering
tags: [quality-engineering, testing, agile, devops, enterprise-transformation]
excerpt: Legacy QA operating models create predictable testing failures; modern quality engineering requires earlier, continuous quality ownership.
imported_on: 2026-03-08
import_method: manual_archive_import
needs_review: false
import_notes: Full body provided by author and normalized to markdown.
status: imported
---

Is a retro approach to QA cramping your enterprise transformation? Plenty of '80s trends are back, but old-school QA practices should not be.

Lean agile software development enables rapid feature delivery, but rapid iteration should not come at the expense of quality. In the 1980s, borrowing ideas from manufacturing and the Deming movement, organizations introduced QA as a distinct organizational function focused on process monitoring and testing.

Fast forward to today: organizations are under pressure to deliver increasingly sophisticated features at much higher speed. Many have evolved development and operations, but traditional QA practices often remain structurally unchanged.

Agile's core principles (adaptive planning, evolutionary development, continuous improvement, and rapid response to change) do not align well with siloed QA models. The result is predictable testing flaws that impact scope, speed, and quality.

## QA Testing Flaws: The Scope, Speed, Quality Tradeoff

In a traditional model:

- developers write code
- code is handed to testers for defect discovery
- bugs are reported back
- developers context-switch from new work to rework

This cycle repeats until bug severity is considered acceptable or release pressure forces a cutoff.

When leadership debates scope/speed/quality tradeoffs, the deeper question is often ignored: why does this tradeoff exist in the first place?

Do developers and testers need to work in strict handoff cycles, with one team coding and the other exclusively finding bugs?

## QA Bottlenecks

Over the past decade, organizations have improved flow with lean and DevOps practices such as CI/CD. Development and operations have evolved significantly, but QA often remains in a legacy structure.

That disconnect slows delivery and creates bottlenecks. QA can improve code quality, but siloed QA alone does not solve the structural tradeoff problem.

Organizations benefit most when DevOps transformation includes a QA operating model reboot that removes unnecessary handoffs.

## QA Safety Net

Traditional QA can unintentionally become a safety net that encourages weaker first-pass developer quality.

Developers assume another group will run exhaustive tests and return required changes. A process intended as a final check becomes the first line of defense.

This model persists because many organizations assume developers cannot reliably build high-quality code from the start.

What if QA focused on higher-order work that accelerates delivery instead?

## Shift Left Testing

Shift-left testing aims to move testing earlier in the SDLC, often by embedding QA resources into scrum teams and increasing automation during sprints.

This can help, but in many cases it shifts bottlenecks earlier rather than eliminating them. A single QA automation specialist frequently cannot keep up with multiple developers, and teams still face automation capacity constraints.

Without a solid, integrated DevOps pipeline, this approach alone does not deliver consistent quality improvements or faster release flow.

To make shift-left real:

1. Every code push should include corresponding testing updates (unit, functional, security, performance).
2. This must be part of each story's definition of done.
3. QA cannot remain an overloaded shared service stretched across many teams.
4. Continuous unattended testing requires strong platform and pipeline integration.

## Continuous Unattended Automation

CI/CD can dramatically speed delivery, but manual-heavy testing portfolios create new bottlenecks.

If an organization is manually executing thousands of scripts, throughput stalls even with improved development practices.

Many enterprises split development and testing across different vendors. In these models, outsourced testing structures can disincentivize automation because manual testing scale can be commercially favorable.

Even after automation adoption, challenges remain:

- test suites rarely cover every scenario
- framework ownership is often concentrated in a few people
- automation primarily validates coded scenarios, not holistic quality dimensions

Automation is critical, but not sufficient by itself.

## Upskilling

Upskilling (reskilling) is another major trend, where manual testers transition into technical engineering roles.

The goal is directionally right, but outcomes are uneven. In practice, many manual testers have not been set up with the programming foundation needed for modern cross-functional engineering roles.

## What's Next?

Enterprises should automate as much testing (and other manual work) as possible so features can move from development to production with minimal lag.

Shift-left practices, automation, and upskilling all help. But solving persistent QA flaws requires deeper assumption changes in operating model, roles, and accountability.

Traditional QA cannot continue unchanged. The next step is quality engineering transformation.

Related:

- [Why Enterprise Quality Is Broken (and Why Many Enterprises Have No Idea)](2018-11-13-why-enterprise-quality-is-broken-and-why-many-enterprises-have-no-idea.md)
