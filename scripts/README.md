# Repository Tooling

Operational scripts for schema enforcement, metadata generation, and deterministic content normalization.

## Command Guide

| Script | Primary Function | Typical Use |
|---|---|---|
| `check_all.sh` | Runs normalization, generation, and validation pipeline end-to-end | One-command pre-commit quality gate |
| `validate_content.py` | Validates writing frontmatter, filename conventions, taxonomy alignment, and writing data files | Pre-commit / CI guardrail for writing content |
| `validate_speakers.py` | Validates `data/speakers.json` structure, speaker-talk references, and field formatting rules | Pre-commit / CI guardrail for speaking data |
| `fix_content.py` | Rewrites writing frontmatter to required schema and regenerates writing index/tag/redirect artifacts | Bulk normalization after imports or manual edits |
| `build_speaking_index.py` | Regenerates speaking index markdown from `data/speakers.json` | Refresh speaking portfolio pages after talk updates |

## Recommended Workflow

1. Apply content/data updates.
2. Run generation/normalization scripts as needed.
3. Run validators before commit.

```bash
./scripts/check_all.sh
```

## Script Reference

### `check_all.sh`
Actions:
- run `fix_content.py`
- run `build_speaking_index.py`
- run `validate_content.py`
- run `validate_speakers.py`

Run:
```bash
./scripts/check_all.sh
```

### `validate_content.py`
Checks:
- writing frontmatter schema and key order
- filename/date/slug/category consistency
- `data/article-index.json` consistency with markdown files
- `data/tags.json` count accuracy
- `data/redirects.json` route consistency

Run:
```bash
python3 scripts/validate_content.py
```

### `validate_speakers.py`
Checks:
- `data/speakers.json` root object and required arrays
- speaker schema (`id`, profile fields, topic/profile arrays)
- talk schema (`speaker_id`, session/event metadata, URL/date/time rules)
- referential integrity and duplicate talk keys

Run:
```bash
python3 scripts/validate_speakers.py
```

### `fix_content.py`
Actions:
- normalize frontmatter to required schema
- enforce author/status defaults
- normalize tags and naming
- align files to `YYYY-MM-DD-slug.md`
- regenerate writing metadata files

Run:
```bash
python3 scripts/fix_content.py
```

Dry run:
```bash
python3 scripts/fix_content.py --dry-run
```

### `build_speaking_index.py`
Actions:
- generate `content/speaking/README.md`
- generate `content/speaking/<speaker-id>.md` engagement table sections

Run:
```bash
python3 scripts/build_speaking_index.py
```
