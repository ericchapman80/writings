---
title: InnerSource as an Enterprise Accelerator to Build a Culture of Collaboration
date: 2019-03-19
author: Eric Chapman
slug: innersource-as-an-enterprise-accelerator-to-build-a-culture-of-collaboration
category: engineering-leadership
tags: [innersource, collaboration, engineering-leadership, developer-experience, enterprise-transformation]
excerpt: InnerSource can improve velocity and code quality by applying open source contribution patterns inside large enterprises.
imported_on: 2026-03-08
import_method: manual_archive_import
needs_review: false
import_notes: Full body provided by author and normalized to markdown.
status: imported
---

We'll talk about what InnerSource is, how it works, and why enterprise organizations should embrace it. We'll also share tips about how organizations can get started.

Enterprise organizations often want to encourage more collaboration among internal teams and even consider open sourcing some in-house software (often called InnerSource). However, many organizations are not sure what is involved or where to start.

In this guide, I'll cover what InnerSource is, how it works, why enterprise organizations should adopt it, and how to get started.

## What Is InnerSource?

At many large organizations, each department behaves like its own entity, building proprietary applications and frameworks. A common barrier is locked-down source repositories, where only one team can access and modify its code.

InnerSource disrupts this pattern. The term was coined by Tim O'Reilly to describe applying open source principles inside an enterprise.

InnerSource is a development methodology where engineers build proprietary software using open source best practices. The InnerSource Commons community, founded by Danese Cooper in 2015, is one example of this movement.

InnerSource encourages innovation and contribution by making it easier for teams to reuse internal code rather than rebuilding from scratch. Documentation quality also improves transparency and shared understanding.

## InnerSource Borrows from Open Source

Many developers already work in open source communities, and InnerSource applies those lessons internally.

Instead of each business unit creating isolated frameworks, teams can share and reuse code within the enterprise boundary. This helps break down silos and build a stronger collective knowledge base.

In open source fashion:

- projects can be forked for team-specific use cases
- communication and documentation are first-class concerns
- improvements should flow back to the primary branch via pull requests

Continuous integration and unit testing are essential in both open source and InnerSource models. Pull requests should include tests, and tests should pass before merge.

## InnerSource Benefits

Without a shared internal hub, enterprise teams frequently rebuild solutions that already exist. This duplication is expensive and common.

Examples of duplicated capability often include:

- CI/CD pipelines
- automated testing frameworks
- authentication services
- communication services
- UI style systems

Organizations adopt InnerSource to:

- encourage knowledge sharing across organizational units
- reduce duplicate development and increase reuse
- improve software quality and delivery speed
- broaden developer contribution opportunities
- accelerate onboarding
- create a path toward selective open source contribution

## How to Build an InnerSource Culture

InnerSource requires a culture of openness.

Transformation happens when teams adopt new ways of working: open communication, fast feedback loops, transparency, continuous learning, and continuous process improvement.

Some teams may hesitate to share code quality that is still evolving. That is why psychological safety is critical. If incomplete or imperfect code leads to blame, innovation slows and collaboration erodes.

## How to Find and Use InnerSource Projects

Store applications from lines of business in a well-known community location.

Key steps:

1. Establish an InnerSource hub (for example, GitHub, GitLab, or Bitbucket).
2. Move projects into the InnerSource hub with SCM admin support.
3. Adopt consistent project naming.
4. Create high-quality README files.
5. Define a clear contribution mechanism.

## InnerSource Project Best Practices

To use InnerSource effectively, establish clear roles, responsibilities, and governance.

Typical roles:

- Project Master: accountable for project direction and best-practice adherence.
- Maintainers: manage project operations and key decisions.
- Contributors: developers/testers who submit features and fixes.

Recommended engineering practices:

- Unit tests for every commit
- Strong repository documentation and decision context
- Neutral package/namespace naming that avoids internal org leakage
- CI quality gates on compile, tests, security scans, and code quality checks

Reference example:

- A GitOps-style InnerSource reference implementation can be used as a starting point for contribution workflows and governance standards.

## Is InnerSource Right for Your Organization?

InnerSource helps teams build faster and collaborate more effectively, improving code quality and documentation quality.

When organizations adopt InnerSource well, contribution becomes broad-based across roles and seniority.

Five key questions to assess readiness:

1. Does the organization support open, transparent collaboration?
2. Do teams use CI tooling on a common engineering platform?
3. Can teams contribute across organizational boundaries?
4. Do cross-functional communities already exist?
5. Do leadership teams actively champion engineering initiatives?

For organizations that can meet these conditions, InnerSource can reduce duplication, improve development quality, and increase engineering efficiency.

I have much more to share on this topic, including a more technical follow-up.
