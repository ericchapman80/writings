# Website Blueprint

## Objective

Design a high-signal personal site that converts writing into speaking, advisory, and consulting opportunities while preserving long-term content ownership.

This blueprint assumes:

- repository content is the source of truth
- future implementation uses React/Next.js
- deployment target is low-cost/free hosting (for example, Vercel)

## Primary Outcomes

1. Establish clear authority in enterprise AI, platform engineering, and quality transformation.
2. Improve discoverability and engagement with writing content.
3. Convert qualified traffic into speaking and consulting inquiries.
4. Build durable distribution infrastructure for future books/newsletters.

## Audience Segments

- Engineering leaders and executives
- Platform/DevOps leaders
- Quality engineering and transformation teams
- Conference organizers
- Potential advisory/consulting buyers

## Information Architecture (v1)

- `/` Home
- `/writing` Writing index
- `/writing/[slug]` Article page
- `/speaking` Speaking index
- `/speaking/[slug]` Session detail page
- `/about` About and bio
- `/work-with-me` Services and inquiry
- `/newsletter` Newsletter capture page

## Visual Direction

- Typography-forward and content-first
- Quiet but premium visual tone
- Ample whitespace, readable line lengths
- Minimal chrome, high scanability
- Strong CTA hierarchy without aggressive marketing aesthetics

## Page Wireframes

### 1) Home (`/`)

#### Block A: Hero

- Headline: one-sentence positioning statement
- Subhead: what you help organizations achieve
- Primary CTA: `Read Writing`
- Secondary CTA: `Book a Speaking Conversation`

#### Block B: Authority Snapshot

- 3-4 short proof points (for example: conferences, transformations, focus domains)
- Optional logo strip (events/organizations) in later phase

#### Block C: Featured Writing

- 3-6 featured articles
- Each card: title, date, category, 1-line excerpt
- CTA: `View All Writing`

#### Block D: Speaking Highlights

- 3 recent talks from `data/speakers.json`
- Each row: date, title, event, link
- CTA: `View Speaking Portfolio`

#### Block E: Newsletter CTA

- Simple value proposition + email form
- Low-friction opt-in

#### Block F: Work With Me

- 2-3 service lanes:
  - speaking
  - advisory
  - consulting
- CTA: `Start a Conversation`

### 2) Writing Index (`/writing`)

#### Block A: Page Intro

- One-line summary of writing purpose and topic focus

#### Block B: Filters

- category filter
- tag filter
- optional year filter

#### Block C: Article List

- reverse chronological listing
- each item includes:
  - title
  - date
  - category
  - tags
  - excerpt
  - read time (optional)

#### Block D: Pagination or Load More

- simple pagination first

### 3) Article Page (`/writing/[slug]`)

#### Block A: Article Header

- title
- publish date
- category
- tags
- optional “updated date” (future versioning support)

#### Block B: Article Body

- high legibility typography
- anchor link support for headings (optional)

#### Block C: End-of-Article CTA

- `Subscribe to Newsletter`
- `Book Eric for Speaking`

#### Block D: Related Content

- 3 related posts by tag/category

### 4) Speaking Index (`/speaking`)

#### Block A: Speaker Overview

- short speaker bio
- key topic areas
- downloadable media kit (future)

#### Block B: Engagement Table

- date, session title, event, co-speakers, source link
- sourced from `data/speakers.json`

#### Block C: Topic Clusters

- enterprise AI
- developer experience
- platform engineering
- quality engineering

#### Block D: Speaking CTA

- `Invite Eric to Speak`
- concise form or email link

### 5) Speaking Session Detail (`/speaking/[slug]`)

#### Block A: Session Metadata

- title, event, date/time, location, co-speakers

#### Block B: Session Abstract

- key themes
- who this talk is for

#### Block C: Assets (future)

- slides
- recording
- related article links

### 6) About (`/about`)

#### Block A: Narrative Bio

- leadership trajectory
- operating philosophy
- focus areas and outcomes

#### Block B: Expertise Areas

- concise bullets tied to audience pain points

#### Block C: Social Proof (future)

- event highlights
- notable transformations
- testimonials

### 7) Work With Me (`/work-with-me`)

#### Block A: Engagement Types

- keynote speaking
- executive advisory
- consulting engagements

#### Block B: Fit Criteria

- who you work best with
- problem statements you solve

#### Block C: Engagement Request

- short intake form
- clear response expectations

### 8) Newsletter (`/newsletter`)

#### Block A: Value Proposition

- what subscribers get
- cadence expectation

#### Block B: Signup Form

- email only first

#### Block C: Archive Preview

- links to recent editions (future)

## Conversion and CTA Strategy

- Primary conversion: speaking/advisory inquiry
- Secondary conversion: newsletter subscription
- Tertiary conversion: deep writing engagement

CTA placement:

- header nav
- home hero
- end-of-article
- speaking pages
- footer

## Content-to-Page Mapping

Use existing repository assets:

- Writing pages: `content/writing/**`
- Speaking data: `data/speakers.json`
- Speaking markdown summaries: `content/speaking/**`
- Taxonomy/index pages: `data/article-index.json`, `data/tags.json`

## SEO and Metadata (v1)

- unique title + description per page
- OpenGraph/Twitter cards
- canonical URLs
- XML sitemap
- RSS feed for writing
- schema markup for articles and events (phase 2)

## Analytics (v1)

- page views
- top entry pages
- article-to-CTA click rate
- speaking page conversion events
- newsletter conversion rate

## Delivery Plan (Implementation Later)

### Phase 1

- Home
- Writing index + article pages
- Speaking index
- About
- baseline SEO

### Phase 2

- Work With Me page + intake form
- Newsletter page + provider integration
- richer speaking session pages

### Phase 3

- syndication and version-aware publishing automation
- performance and conversion optimization
- structured data enhancements

## Out of Scope (for now)

- actual Next.js scaffolding
- deployment pipeline implementation
- channel publishing automation

These will be addressed in a later implementation phase.
