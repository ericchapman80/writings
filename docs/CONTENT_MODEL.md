# Content Model

## Objectives

- Preserve writing in durable markdown.
- Keep metadata rich enough for future website, search, newsletters, and republishing.
- Maintain simple structure without early over-engineering.

## Frontmatter Schema

Each article must use this exact key order:

- `title`
- `date`
- `author`
- `slug`
- `category`
- `tags`
- `excerpt`
- `imported_on`
- `import_method`
- `needs_review`
- `import_notes`
- `status`

## Taxonomy

Primary categories:

- `ai-enterprise-strategy`
- `developer-experience`
- `engineering-leadership`
- `platform-devops`
- `quality-engineering`
- `enterprise-transformation`

Rules:

- One primary category per article (folder placement).
- Cross-cutting themes handled via `tags`.
- Slugs are canonical, lowercase, hyphenated.

## Data Files

- `data/article-index.json`: list view and machine-readable routing source.
- `data/tags.json`: normalized tag registry and counts.
- `data/redirects.json`: canonical route -> local markdown path mapping.
- `data/speakers.json`: speaker profiles and talk/session metadata for speaking portfolio use cases.

## Speaking Content

- Speaker profile markdown files live in `content/speaking/`.
- `data/speakers.json` is the structured source for speaker and session cards.
- When source pages are inaccessible, entries should set `needs_review: true` and include clear `import_notes`.

## Validation

Run:

```bash
python3 scripts/validate_content.py
```

The validator enforces frontmatter schema, filename/category conventions, and consistency between markdown files and JSON metadata.
