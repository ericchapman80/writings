#!/usr/bin/env python3
"""Build speaking markdown indexes from data/speakers.json."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "speakers.json"
SPEAKING_DIR = ROOT / "content" / "speaking"
README_FILE = SPEAKING_DIR / "README.md"
ENGAGEMENTS_DIR = SPEAKING_DIR / "engagements"


def slugify(value: str) -> str:
    value = value.replace("&", " and ")
    value = re.sub(r"[’']", "", value)
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def talk_filename(talk: dict) -> str:
    title_slug = slugify(talk["title"])
    if talk.get("date"):
        return f"{talk['date']}-{title_slug}.md"
    return f"{talk['event_year']}-{slugify(talk['event'])}-{title_slug}.md"


def source_label(url: str) -> str:
    if "sched.com" in url:
        return "Sched"
    if "pluralsight.com" in url:
        return "Event"
    if url.endswith(".pdf"):
        return "PDF"
    return "Link"


def sort_key(talk: dict):
    date = talk.get("date")
    if date:
        dt = datetime.strptime(date, "%Y-%m-%d")
        return (0, -int(dt.strftime("%Y%m%d")), talk["title"])
    return (1, -talk["event_year"], talk["title"])


def date_label(talk: dict) -> str:
    return talk["date"] if talk.get("date") else f"TBD {talk['event_year']}"


def time_label(talk: dict) -> str:
    start = talk.get("start_time_local")
    end = talk.get("end_time_local")
    tz = talk.get("timezone")
    if start and end and tz:
        return f"{start}-{end} ({tz})"
    if start and end:
        return f"{start}-{end}"
    return "TBD"


def speaker_markdown(speaker: dict, talks: list[dict]) -> str:
    role = speaker.get("headline", "").split(",", 1)[0].strip() or ""
    organization = ""
    if "," in speaker.get("headline", ""):
        organization = speaker["headline"].split(",", 1)[1].strip()

    topics = ", ".join(speaker.get("topics", []))
    lines = [
        "---",
        f"name: {speaker['name']}",
        f"slug: {speaker['id']}",
        f"role: {role}",
        f"organization: {organization}",
        f"topics: [{topics}]",
        f"imported_on: {speaker.get('imported_on', datetime.now(UTC).strftime('%Y-%m-%d'))}",
        "import_method: generated_from_data_speakers_json",
        f"needs_review: {'true' if speaker.get('needs_review', False) else 'false'}",
        f"import_notes: {speaker.get('import_notes', '').strip() or 'Generated from data/speakers.json.'}",
        "status: imported",
        "---",
        "",
        "## Overview",
        "",
        speaker.get("bio", ""),
        "",
        "## Focus Areas",
        "",
    ]

    for topic in speaker.get("topics", []):
        lines.append(f"- {topic.title()}")

    lines.extend([
        "",
        "## Engagement Highlights",
        "",
        "| Date | Time | Session | Event | Location | Co-speakers | Source |",
        "|---|---|---|---|---|---|---|",
    ])

    for talk in sorted(talks, key=sort_key):
        co = ", ".join(talk.get("co_speakers", [])) or "-"
        loc = talk.get("room") or "TBD"
        source = f"[{source_label(talk['source_url'])}]({talk['source_url']})"
        lines.append(
            f"| {date_label(talk)} | {time_label(talk)} | {talk['title']} | {talk['event']} | {loc} | {co} | {source} |"
        )

    lines.extend(["", "## Session Pages", ""])
    for talk in sorted(talks, key=sort_key):
        fn = talk_filename(talk)
        lines.append(f"- [{talk['title']}](./engagements/{fn})")

    lines.append("")
    return "\n".join(lines)


def read_data() -> dict:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def build_readme(speakers: list[dict], talks: list[dict]) -> str:
    lines = [
        "# Speaking Portfolio",
        "",
        "Structured speaker and engagement content curated for enterprise-facing thought leadership.",
        "",
        "## Speakers",
        "",
        "| Name | Profile | Focus Areas |",
        "|---|---|---|",
    ]

    for s in sorted(speakers, key=lambda x: x["name"]):
        topics = ", ".join(t.title() for t in s.get("topics", [])[:4])
        lines.append(f"| {s['name']} | [View](./{s['id']}.md) | {topics} |")

    lines.extend(
        [
            "",
            "## Engagement Index",
            "",
            "| Date | Session | Event | Co-speakers | Source | Details |",
            "|---|---|---|---|---|---|",
        ]
    )

    for talk in sorted(talks, key=sort_key):
        fn = talk_filename(talk)
        co = ", ".join(talk.get("co_speakers", [])) or "-"
        source = f"[{source_label(talk['source_url'])}]({talk['source_url']})"
        lines.append(
            f"| {date_label(talk)} | {talk['title']} | {talk['event']} | {co} | {source} | [Open](./engagements/{fn}) |"
        )

    lines.extend(
        [
            "",
            "## Data Authority",
            "",
            "- Canonical metadata source: `data/speakers.json`.",
            "- Portfolio pages are generated to maintain consistency and reduce manual drift.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    doc = read_data()
    speakers = doc.get("speakers", [])
    talks = doc.get("talks", [])

    SPEAKING_DIR.mkdir(parents=True, exist_ok=True)
    ENGAGEMENTS_DIR.mkdir(parents=True, exist_ok=True)

    README_FILE.write_text(build_readme(speakers, talks), encoding="utf-8")

    talks_by_speaker: dict[str, list[dict]] = {}
    for talk in talks:
        talks_by_speaker.setdefault(talk["speaker_id"], []).append(talk)

    for speaker in speakers:
        speaker_file = SPEAKING_DIR / f"{speaker['id']}.md"
        speaker_file.write_text(
            speaker_markdown(speaker, talks_by_speaker.get(speaker["id"], [])),
            encoding="utf-8",
        )

    print("Wrote content/speaking/README.md")
    for speaker in speakers:
        print(f"Wrote content/speaking/{speaker['id']}.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
