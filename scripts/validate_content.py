#!/usr/bin/env python3
"""Validate writing content schema and metadata consistency."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime
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

EXPECTED_INDEX_KEYS = ["title", "date", "slug", "category", "tags", "filename"]
EXPECTED_AUTHOR = "Eric Chapman"
EXPECTED_STATUS = "imported"
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


def _parse_scalar(text: str):
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


def parse_frontmatter(md_path: Path) -> dict:
    raw = md_path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ValueError("Missing opening frontmatter delimiter")

    parts = raw.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError("Missing closing frontmatter delimiter")

    fm_lines = parts[0].splitlines()[1:]
    fm: dict[str, object] = {}
    key_order: list[str] = []

    for line in fm_lines:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        fm[key] = _parse_scalar(value)
        key_order.append(key)

    fm["_key_order"] = key_order
    return fm


def validate_content() -> list[str]:
    errors: list[str] = []
    files = sorted(CONTENT_ROOT.glob("*/*.md"))
    if not files:
        return ["No content files found under content/writing/<category>/*.md"]

    meta_by_filename: dict[str, dict] = {}
    tag_counter: Counter[str] = Counter()

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        category_dir = path.parent.name
        filename = path.name
        fm: dict

        try:
            fm = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue

        key_order = fm.pop("_key_order", [])
        if key_order != EXPECTED_FRONTMATTER_KEYS:
            errors.append(
                f"{rel}: frontmatter key order mismatch. "
                f"Expected {EXPECTED_FRONTMATTER_KEYS}, got {key_order}"
            )

        missing = [k for k in EXPECTED_FRONTMATTER_KEYS if k not in fm]
        extra = [k for k in fm.keys() if k not in EXPECTED_FRONTMATTER_KEYS]
        if missing:
            errors.append(f"{rel}: missing frontmatter keys: {missing}")
        if extra:
            errors.append(f"{rel}: unexpected frontmatter keys: {extra}")

        date = str(fm.get("date", ""))
        slug = str(fm.get("slug", ""))
        category = str(fm.get("category", ""))
        author = str(fm.get("author", ""))
        status = str(fm.get("status", ""))
        imported_on = str(fm.get("imported_on", ""))
        tags = fm.get("tags")

        if author != EXPECTED_AUTHOR:
            errors.append(f"{rel}: author must be '{EXPECTED_AUTHOR}'")
        if status != EXPECTED_STATUS:
            errors.append(f"{rel}: status must be '{EXPECTED_STATUS}'")
        if category not in ALLOWED_CATEGORIES:
            errors.append(f"{rel}: invalid category '{category}'")
        if category != category_dir:
            errors.append(f"{rel}: category '{category}' does not match folder '{category_dir}'")
        if not DATE_RE.match(date):
            errors.append(f"{rel}: invalid date format '{date}' (expected YYYY-MM-DD)")
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                errors.append(f"{rel}: invalid calendar date '{date}'")

        if not DATE_RE.match(imported_on):
            errors.append(f"{rel}: invalid imported_on format '{imported_on}'")

        if not SLUG_RE.match(slug):
            errors.append(f"{rel}: invalid slug '{slug}'")

        expected_filename = f"{date}-{slug}.md"
        if filename != expected_filename:
            errors.append(f"{rel}: filename must be '{expected_filename}'")

        if not isinstance(tags, list):
            errors.append(f"{rel}: tags must be a list")
            tags = []
        else:
            for tag in tags:
                if not isinstance(tag, str) or not SLUG_RE.match(tag):
                    errors.append(f"{rel}: invalid tag '{tag}'")
                else:
                    tag_counter[tag] += 1

        if not isinstance(fm.get("needs_review"), bool):
            errors.append(f"{rel}: needs_review must be true/false")

        meta_by_filename[rel] = {
            "title": fm.get("title", ""),
            "date": date,
            "slug": slug,
            "category": category,
            "tags": tags,
            "filename": rel,
        }

    # Validate article index
    try:
        index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{INDEX_FILE.relative_to(ROOT).as_posix()}: invalid JSON ({exc})")
        index = []

    if not isinstance(index, list):
        errors.append("data/article-index.json: root must be an array")
        index = []

    if len(index) != len(meta_by_filename):
        errors.append(
            f"data/article-index.json: expected {len(meta_by_filename)} entries, got {len(index)}"
        )

    seen_index_files = set()
    for i, entry in enumerate(index):
        if not isinstance(entry, dict):
            errors.append(f"data/article-index.json[{i}]: entry must be object")
            continue

        keys = list(entry.keys())
        if keys != EXPECTED_INDEX_KEYS:
            errors.append(
                f"data/article-index.json[{i}]: key order mismatch. "
                f"Expected {EXPECTED_INDEX_KEYS}, got {keys}"
            )

        filename = entry.get("filename", "")
        if filename not in meta_by_filename:
            errors.append(f"data/article-index.json[{i}]: unknown filename '{filename}'")
            continue

        seen_index_files.add(filename)
        expected = meta_by_filename[filename]
        for key in EXPECTED_INDEX_KEYS:
            if key == "tags":
                if entry.get(key) != expected[key]:
                    errors.append(
                        f"data/article-index.json[{i}]: tags mismatch for {filename}"
                    )
            else:
                if str(entry.get(key, "")) != str(expected[key]):
                    errors.append(
                        f"data/article-index.json[{i}]: '{key}' mismatch for {filename}"
                    )

    missing_in_index = sorted(set(meta_by_filename.keys()) - seen_index_files)
    if missing_in_index:
        errors.append(f"data/article-index.json: missing filenames {missing_in_index}")

    # Validate tags registry
    try:
        tags_doc = json.loads(TAGS_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"data/tags.json: invalid JSON ({exc})")
        tags_doc = {}

    declared_tags: Counter[str] = Counter()
    tags_arr = tags_doc.get("tags", []) if isinstance(tags_doc, dict) else []
    if not isinstance(tags_arr, list):
        errors.append("data/tags.json: 'tags' must be an array")
        tags_arr = []

    for i, item in enumerate(tags_arr):
        if not isinstance(item, dict):
            errors.append(f"data/tags.json tags[{i}]: must be object")
            continue
        tag = item.get("tag")
        count = item.get("count")
        if not isinstance(tag, str) or not SLUG_RE.match(tag):
            errors.append(f"data/tags.json tags[{i}]: invalid tag '{tag}'")
            continue
        if not isinstance(count, int) or count < 1:
            errors.append(f"data/tags.json tags[{i}]: invalid count '{count}'")
            continue
        declared_tags[tag] = count

    if declared_tags != tag_counter:
        errors.append(
            f"data/tags.json: tag counts do not match content. expected={dict(tag_counter)} got={dict(declared_tags)}"
        )

    # Validate redirects
    try:
        redirects = json.loads(REDIRECTS_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"data/redirects.json: invalid JSON ({exc})")
        redirects = {}

    if not isinstance(redirects, dict):
        errors.append("data/redirects.json: root must be an object")
        redirects = {}

    expected_routes = {
        f"/writing/{meta['slug']}": f"/{meta['filename']}" for meta in meta_by_filename.values()
    }

    if redirects != expected_routes:
        errors.append("data/redirects.json: mapping does not match /writing/<slug> -> /<filename>")

    return errors


def main() -> int:
    errors = validate_content()
    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Validation passed: content schema and metadata are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
