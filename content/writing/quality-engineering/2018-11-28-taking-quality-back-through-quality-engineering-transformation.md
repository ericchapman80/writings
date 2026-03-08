---
title: Taking Quality Back Through Quality Engineering Transformation
date: 2018-11-28
author: Eric Chapman
slug: taking-quality-back-through-quality-engineering-transformation
category: quality-engineering
tags: [quality-engineering, transformation, enterprise-quality, leadership]
excerpt: A call to shift from legacy QA approaches toward integrated quality engineering transformation.
imported_on: 2026-03-08
import_method: manual_archive_import
needs_review: false
import_notes: Full body provided by author and normalized to markdown.
status: imported
---

In the age of lean agile continuous delivery, is there also a leaner, more agile approach to QA? And if so, what does that approach look like?

In my last post, I highlighted common QA testing flaws. Those flaws create bug-ridden code, stop-and-go flow of work, and costly context switching.

All of this raises two questions:

1. In the age of lean agile continuous delivery, is there also a leaner, more agile approach to QA?
2. If so, what does it look like?

To answer that, I ask another question: why aren't developers writing code correctly from the start? Questioning assumptions about developer capabilities is often the key to enterprise-wide quality engineering transformation.

## Agile Quality Engineering Requires Engineers to Code and Test

Conventional wisdom says developers cannot test. The logic goes: if they could test, they would build it right the first time. Because they don't, they can't.

This circular reasoning traps teams in binary roles:

- developers write code
- testers find and report defects

Developers become conditioned to think quality belongs to the test team or test automation tooling, not to themselves.

As a result, developers stop learning from their own mistakes, and organizations build inefficiency into delivery through siloed responsibilities.

In practice, one engineer acting as both developer and quality engineer is often more effective than multiple specialists working in sequence.

## Moving from Traditional QA to Quality Engineering

Can developers build code correctly the first time? Can agile QE reduce scope/speed/quality tradeoffs? I believe yes to both.

Quality engineering enables development, testing, and bug fixes in parallel. Traditional non-functional testing often happens too late for teams to respond to performance and security findings without delay.

When developers can test effectively and are supported by a strong DevOps pipeline, feedback loops tighten and rework cycles shrink. But this only works when delivery teams carry both responsibility and accountability for quality.

In agile QE, combining development and testing roles is pragmatic: it is generally easier to teach developers modern testing than to turn manual testers into developers at scale.

The goal is built-in quality so that every commit triggers:

- unit testing
- functional testing
- baseline non-functional requirement (NFR) checks

With chatops and fast feedback, teams lower MTTR and improve coding behavior over time.

## How Does Quality Engineering Work?

Teams develop QE skills through education and disciplined practice.

BDD and TDD can speed feedback cycles, improve communication, and introduce automation before coding begins.

A common pattern:

- teams run story sessions from the user perspective
- scenarios are written in Gherkin and become executable specifications
- scenarios become acceptance tests and automation scripts

This is Acceptance Test Driven Development (ATDD).

Product owners and scrum masters can also be coached to write Gherkin-based tests and trigger them easily, lowering the barrier to automation and strengthening shared understanding.

## Quality Engineering Transformation Best Practices

With QE, focus moves from defect discovery to defect prevention through built-in quality.

### Step 1: Make Everyone Responsible for Quality

Transitioning from QA to QE is not instant. Teams often need coaching and strong DevOps foundations.

A QE coach can help developers learn tools, patterns, and practices while aligning the whole team on quality ownership.

### Step 2: Establish Clear Acceptance Criteria Up Front

Clear acceptance criteria reduce rejection cycles.

Exploratory testing complements automation. Pairing sessions and testing notes help developers reason through risk and improve test quality.

Avoid purely prescriptive scripted testing; include heuristic tips that encourage critical thinking.

### Step 3: Take Peer Reviews Seriously

If peer reviews are weak, teams fall back into the old QA safety-net behavior.

Developers need to own testing from story to production, with team accountability and coach support.

### Step 4: Implement Proven Accelerators

Organizations should leverage open, vendor-agnostic accelerators and experienced partners that have already embedded continuous testing and QE principles.

Once teams adopt a QE mindset, accelerators can speed implementation of baseline performance and other NFR quality gates across all commits.

## Quality Engineering Transformation Fosters Continuous Innovation

Pop quiz: you have 50 developers and must ship high-quality releases every two weeks. How many QA testers do you need?

Answer: the same 50 people doing the development work.

The point is not eliminating quality work. The point is integrating quality ownership directly into software creation.

I've participated in multiple QE transformations where manual, repetitive tasks were removed, speed increased, and quality improved because more delivery horsepower was directed at higher-order problems.

Tools such as SonarQube help teams enforce measurable quality gates, maintain audit trails, and provide fast feedback with every commit.

QE and DevOps transformations also align naturally with InnerSource, enabling teams to share practices and accelerate high-quality delivery across organizational boundaries.

## QE Revolutionizes Development, Operations, and Testing

QE transformation is a major structural shift away from traditional silos. Ownership of development, operations, and quality moves into delivery teams and individual engineers.

Done well, these practices:

- increase developer ownership
- remove unnecessary manual testing steps
- use automation strategically
- improve release quality and speed
- foster continuous innovation

Organizations that adopt these practices return testing responsibility to developers, prevent bugs rather than detect them late, and fundamentally improve how engineering teams deliver software.
