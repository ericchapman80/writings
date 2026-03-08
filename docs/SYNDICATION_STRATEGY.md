# Syndication Strategy

## Purpose

Define how this repository publishes writing content across multiple destinations while keeping this repo as the single source of truth.

## Publishing Model

- Canonical source: this repository
- Canonical destination (future): personal website
- Syndicated destinations: LinkedIn, Medium, Substack
- Control model: automation-assisted, human-approved for external platforms

## Channel Pros and Cons

| Channel | Strengths | Tradeoffs | Recommended Use |
|---|---|---|---|
| Personal Website (future) | Full control, canonical SEO authority, durable archive | Requires build/hosting/SEO ownership | Primary canonical publication target |
| LinkedIn | Strong professional reach and engagement loops | Limited formatting/control, platform constraints | Executive audience distribution and discussion |
| Medium | Built-in distribution and clean reader UX | Platform dependency, weaker brand ownership | Broader reach and discoverability |
| Substack | Direct subscriber relationship, newsletter + archive | Requires cadence discipline, platform dependency | Serialized essays and recurring thought leadership |

## Canonical and SEO Policy

1. Publish canonical version to personal website first (when available).
2. Cross-post to external channels with canonical attribution back to personal site.
3. Track all published URLs and versions in article metadata.
4. Avoid unmanaged content divergence across channels.

## Syndication Modes

| Mode | Description | Best For |
|---|---|---|
| Full-text Cross-post | Entire article syndicated to each channel | Reach maximization |
| Teaser + Linkback | Summary/excerpt externally, full article on canonical site | SEO focus and owned-traffic growth |
| Channel-tailored Variant | Core body is same, intro/CTA adjusted per platform | Audience optimization |

## Recommended v1 Operating Policy

1. Use full-text publication to website (future).
2. Use channel-tailored variant for LinkedIn.
3. Use full-text or lightly edited full-text for Medium/Substack.
4. Require manual approval for all non-website publishing actions.

## Workflow (v1)

1. Author edits article in this repo.
2. Content validation pipeline passes (`./scripts/check_all.sh`).
3. Publish manifest generated from changed articles.
4. Reviewer approves target channels.
5. Publisher workflow executes per channel adapter.
6. Article metadata is updated with publish URLs and published versions.

## Governance

- Source of truth is always repository markdown.
- External platform edits must be back-ported into this repo or rejected.
- Versioning and publish status must be machine-readable.

## Future Enhancements

- Scheduled republishing windows.
- Audience-specific content transforms.
- Per-channel performance telemetry in `data/`.
