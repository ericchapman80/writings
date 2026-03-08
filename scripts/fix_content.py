#!/usr/bin/env python3
"""Auto-fix writing content frontmatter and metadata indexes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_ROOT = ROOT / "content" / "writing"
INDEX_FILE = ROOT / "data" / "article-index.json"
TAGS_FILE = ROOT / "data" / "tags.json"
REDIRECTS_FILE = ROOT / "data" / "redirects.json"

EXPECTED_FRONTMATTER_KEYS = [
    "title",
    "date",
    "author",
    "slug",
    "category",
    "tags",
    "excerpt",
    "imported_on",
    "import_method",
    "needs_review",
    "import_notes",
    "status",
]

ALLOWED_CATEGORIES = {
    "ai-enterprise-strategy",
    "developer-experience",
    "engineering-leadership",
    "platform-devops",
    "quality-engineering",
    "enterprise-transformation",
}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_scalar(text: str):
    text = text.strip()
    if text == "true":
        return True
    if text == "false":
        return False
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",") if item.strip()]
    return text.strip("\"'")


def parse_markdown(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---\n") and "\n---\n" in raw:
        head, body = raw.split("\n---\n", 1)
        fm: dict[str, object] = {}
        for line in head.splitlines()[1:]:
            if not line.strip() or ":" not in line:
                continue
            key, value = line.split(":", 1)
            fm[key.strip()] = parse_scalar(value.strip())
        return fm, body
    return {}, raw


def slugify(value: str) -> str:
    v = value.strip().lower()
    v = re.sub(r"[^a-z0-9]+", "-", v)
    v = re.sub(r"-+", "-", v).strip("-")
    return v


def normalize_date(value: object, fallback: str) -> str:
    s = str(value or "").strip()
    if DATE_RE.match(s):
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return s
        except ValueError:
            pass
    return fallback


def format_value(key: str, value: object) -> str:
    if key == "tags":
        tags = value if isinstance(value, list) else []
        return "[" + ", ".join(tags) + "]"
    if key == "needs_review":
        return "true" if bool(value) else "false"
    return str(value)


def normalize_frontmatter(path: Path, fm: dict[str, object]) -> dict[str, object]:
    parent_category = path.parent.name if path.parent.name in ALLOWED_CATEGORIES else "enterprise-transformation"

    # Filename hints
    stem = path.stem
    date_hint = "1970-01-01"
    slug_hint = slugify(stem)
    m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)$", stem)
    if m:
        date_hint = m.group(1)
        slug_hint = slugify(m.group(2))

    title = str(fm.get("title", "")).strip() or stem.replace("-", " ").title()
    parsed_slug = slugify(str(fm.get("slug", "")).strip()) or slug_hint or slugify(title)
    parsed_date = normalize_date(fm.get("date", ""), date_hint)

    category = str(fm.get("category", "")).strip()
    if category not in ALLOWED_CATEGORIES:
        category = parent_category

    tags = fm.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    cleaned_tags = []
    for t in tags:
        s = slugify(str(t))
        if s and s not in cleaned_tags:
            cleaned_tags.append(s)

    imported_on = normalize_date(fm.get("imported_on", ""), str(date.today()))

    normalized: dict[str, object] = {
        "title": title,
        "date": parsed_date,
        "author": "Eric Chapman",
        "slug": parsed_slug,
        "category": category,
        "tags": cleaned_tags,
        "excerpt": str(fm.get("excerpt", "")).strip(),
        "imported_on": imported_on,
        "import_method": str(fm.get("import_method", "")).strip() or "manual_archive_import",
        "needs_review": bool(fm.get("needs_review", False)),
        "import_notes": str(fm.get("import_notes", "")).strip(),
        "status": "imported",
    }

    return normalized


def write_markdown(path: Path, fm: dict[str, object], body: str, dry_run: bool) -> None:
    lines = ["---"]
    for key in EXPECTED_FRONTMATTER_KEYS:
        lines.append(f"{key}: {format_value(key, fm[key])}")
    lines.append("---")
    output = "\n".join(lines) + "\n\n" + body.lstrip("\n")
    if not dry_run:
        path.write_text(output, encoding="utf-8")


def build_indexes(records: list[dict[str, object]], dry_run: bool) -> None:
    index = [
        {
            "title": r["title"],
            "date": r["date"],
            "slug": r["slug"],
            "category": r["category"],
            "tags": r["tags"],
            "filename": r["filename"],
        }
        for r in sorted(records, key=lambda x: (x["date"], x["slug"]))
    ]

    tag_counts: Counter[str] = Counter()
    for r in records:
        for tag in r["tags"]:
            tag_counts[tag] += 1

    tags_doc = {
        "tags": [
            {"tag": k, "count": v}
            for k, v in sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        ]
    }

    redirects = {
        f"/writing/{r['slug']}": f"/{r['filename']}"
        for r in sorted(records, key=lambda x: x["slug"])
    }

    if dry_run:
        return

    INDEX_FILE.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    TAGS_FILE.write_text(json.dumps(tags_doc, indent=2) + "\n", encoding="utf-8")
    REDIRECTS_FILE.write_text(json.dumps(redirects, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto-fix writing frontmatter and metadata files")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    args = parser.parse_args()

    files = sorted(CONTENT_ROOT.glob("*/*.md"))
    if not files:
        print("No content files found under content/writing/<category>/*.md")
        return 1

    records: list[dict[str, object]] = []
    for path in files:
        fm, body = parse_markdown(path)
        normalized = normalize_frontmatter(path, fm)

        target_dir = CONTENT_ROOT / str(normalized["category"])
        target_name = f"{normalized['date']}-{normalized['slug']}.md"
        target_path = target_dir / target_name

        action = "update"
        if target_path != path:
            action = "move"
            if not args.dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                path.rename(target_path)
            path = target_path

        write_markdown(path, normalized, body, args.dry_run)

        rel = path.relative_to(ROOT).as_posix()
        records.append(
            {
                "title": normalized["title"],
                "date": normalized["date"],
                "slug": normalized["slug"],
                "category": normalized["category"],
                "tags": normalized["tags"],
                "filename": rel,
            }
        )
        print(f"{action}: {rel}")

    build_indexes(records, args.dry_run)
    print(f"wrote: {INDEX_FILE.relative_to(ROOT).as_posix()}")
    print(f"wrote: {TAGS_FILE.relative_to(ROOT).as_posix()}")
    print(f"wrote: {REDIRECTS_FILE.relative_to(ROOT).as_posix()}")
    print("fix complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
