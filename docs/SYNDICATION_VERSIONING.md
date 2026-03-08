# Syndication Versioning (SemVer)

## Goal

Apply software-style versioning to written content so publishing decisions are deterministic and auditable.

## Core Concept

Each article carries a semantic version. Republish behavior is driven by version changes.

- `MAJOR` (`X.0.0`): substantial rewrite or repositioning
- `MINOR` (`x.Y.0`): meaningful additions/updates
- `PATCH` (`x.y.Z`): typo/format/small clarifications

## Frontmatter Extension (Proposed)

Add these fields to each writing article:

```yaml
version: 1.0.0
version_notes:
last_published_version: 1.0.0
publish_policy: selective
published_targets:
  website:
    status: published
    version: 1.0.0
    published_on: 2026-03-08
    url:
  linkedin:
    status: pending
    version:
    published_on:
    url:
  medium:
    status: pending
    version:
    published_on:
    url:
  substack:
    status: pending
    version:
    published_on:
    url:
```

## Republish Rules

| Version Change | Default Action | Typical Channel Behavior |
|---|---|---|
| `PATCH` | Optional republish | Website update; external channels optional |
| `MINOR` | Republish recommended | Website + selected channels |
| `MAJOR` | Republish required | Website + all target channels |

## CI/CD Flow

1. Detect changed articles in PR/push.
2. Validate SemVer field shape.
3. Compare `version` to `last_published_version`.
4. Build `data/publish-queue.json` for changed-version articles.
5. Apply policy rules to determine target channels.
6. Require approval gate for external channel publishing.
7. Execute publisher adapters.
8. Write back publish metadata (`published_targets`, `last_published_version`).

## Pipeline Responsibilities

- Validation stage:
  - valid SemVer
  - version increment required when article body changes
  - metadata completeness for publish targets
- Planning stage:
  - produce publish queue
  - classify change impact (`major`/`minor`/`patch`)
- Publish stage:
  - website (future) can be auto-publish
  - LinkedIn/Medium/Substack initially manual-approval

## Platform Adapter Reality

Not all platforms provide robust "update existing article" APIs.

Design assumption:
- Repo decides publication intent.
- Channel adapter decides operational action:
  - update in place
  - create new item
  - skip and mark manual action required

## Data Artifacts (Proposed)

- `data/publish-queue.json`: pending publish actions from version deltas
- `data/publish-history.json`: immutable publish audit trail
- `data/channel-capabilities.json`: adapter capabilities and constraints

## Rollout Plan

1. Phase 1: Add version fields, validate only.
2. Phase 2: Generate publish queue + manual execution runbook.
3. Phase 3: Implement website auto-publish.
4. Phase 4: Add semi-automated external channel adapters with approvals.

## Guardrails

- No article body change without version increment.
- No external publish without URL/version writeback.
- No manual external edits that are not mirrored to repo source.
