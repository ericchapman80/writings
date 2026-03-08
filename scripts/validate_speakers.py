#!/usr/bin/env python3
"""Validate data/speakers.json schema consistency."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEAKERS_FILE = ROOT / "data" / "speakers.json"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
URL_RE = re.compile(r"^https?://")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED_SPEAKER_KEYS = [
    "id",
    "name",
    "headline",
    "bio",
    "topics",
    "profiles",
    "imported_on",
    "import_method",
    "needs_review",
    "import_notes",
]

REQUIRED_TALK_KEYS = [
    "speaker_id",
    "event",
    "event_year",
    "title",
    "date",
    "start_time_local",
    "end_time_local",
    "timezone",
    "room",
    "co_speakers",
    "source_url",
    "needs_review",
    "import_notes",
]


def _is_date(value: str) -> bool:
    if not DATE_RE.match(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _validate_optional_time(value: object) -> bool:
    if value is None:
        return True
    return isinstance(value, str) and bool(TIME_RE.match(value))


def _validate_optional_text(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() != "")


def validate() -> list[str]:
    errors: list[str] = []

    try:
        doc = json.loads(SPEAKERS_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"data/speakers.json: invalid JSON ({exc})"]

    if not isinstance(doc, dict):
        return ["data/speakers.json: root must be an object"]

    speakers = doc.get("speakers")
    talks = doc.get("talks")

    if not isinstance(speakers, list):
        errors.append("data/speakers.json: 'speakers' must be an array")
        speakers = []
    if not isinstance(talks, list):
        errors.append("data/speakers.json: 'talks' must be an array")
        talks = []

    speaker_ids: set[str] = set()

    for i, speaker in enumerate(speakers):
        prefix = f"speakers[{i}]"
        if not isinstance(speaker, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        missing = [k for k in REQUIRED_SPEAKER_KEYS if k not in speaker]
        if missing:
            errors.append(f"{prefix}: missing keys {missing}")

        sid = speaker.get("id")
        if not isinstance(sid, str) or not ID_RE.match(sid):
            errors.append(f"{prefix}.id: must be kebab-case string")
        elif sid in speaker_ids:
            errors.append(f"{prefix}.id: duplicate id '{sid}'")
        else:
            speaker_ids.add(sid)

        for key in ["name", "headline", "bio", "import_method", "import_notes"]:
            if not isinstance(speaker.get(key), str) or not speaker.get(key).strip():
                errors.append(f"{prefix}.{key}: must be non-empty string")

        imported_on = speaker.get("imported_on")
        if not isinstance(imported_on, str) or not _is_date(imported_on):
            errors.append(f"{prefix}.imported_on: must be YYYY-MM-DD")

        if not isinstance(speaker.get("needs_review"), bool):
            errors.append(f"{prefix}.needs_review: must be boolean")

        topics = speaker.get("topics")
        if not isinstance(topics, list) or not topics:
            errors.append(f"{prefix}.topics: must be a non-empty array")
        else:
            for j, topic in enumerate(topics):
                if not isinstance(topic, str) or not topic.strip():
                    errors.append(f"{prefix}.topics[{j}]: must be non-empty string")

        profiles = speaker.get("profiles")
        if not isinstance(profiles, list) or not profiles:
            errors.append(f"{prefix}.profiles: must be a non-empty array")
        else:
            for j, p in enumerate(profiles):
                pfx = f"{prefix}.profiles[{j}]"
                if not isinstance(p, dict):
                    errors.append(f"{pfx}: must be object")
                    continue
                platform = p.get("platform")
                url = p.get("url")
                if not isinstance(platform, str) or not platform.strip():
                    errors.append(f"{pfx}.platform: must be non-empty string")
                if not isinstance(url, str) or not URL_RE.match(url):
                    errors.append(f"{pfx}.url: must be http(s) URL")

    seen_talk_keys: set[tuple[str, int, str]] = set()
    for i, talk in enumerate(talks):
        prefix = f"talks[{i}]"
        if not isinstance(talk, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        missing = [k for k in REQUIRED_TALK_KEYS if k not in talk]
        if missing:
            errors.append(f"{prefix}: missing keys {missing}")

        speaker_id = talk.get("speaker_id")
        if not isinstance(speaker_id, str) or speaker_id not in speaker_ids:
            errors.append(f"{prefix}.speaker_id: must reference an existing speaker id")

        event = talk.get("event")
        title = talk.get("title")
        source_url = talk.get("source_url")
        for key, value in [("event", event), ("title", title), ("import_notes", talk.get("import_notes"))]:
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{key}: must be non-empty string")

        event_year = talk.get("event_year")
        if not isinstance(event_year, int) or not (2000 <= event_year <= 2100):
            errors.append(f"{prefix}.event_year: must be integer between 2000 and 2100")

        if not isinstance(source_url, str) or not URL_RE.match(source_url):
            errors.append(f"{prefix}.source_url: must be http(s) URL")

        d = talk.get("date")
        if d is not None and (not isinstance(d, str) or not _is_date(d)):
            errors.append(f"{prefix}.date: must be null or YYYY-MM-DD")

        if not _validate_optional_time(talk.get("start_time_local")):
            errors.append(f"{prefix}.start_time_local: must be null or HH:MM")
        if not _validate_optional_time(talk.get("end_time_local")):
            errors.append(f"{prefix}.end_time_local: must be null or HH:MM")

        if not _validate_optional_text(talk.get("timezone")):
            errors.append(f"{prefix}.timezone: must be null or non-empty string")
        if not _validate_optional_text(talk.get("room")):
            errors.append(f"{prefix}.room: must be null or non-empty string")

        co_speakers = talk.get("co_speakers")
        if not isinstance(co_speakers, list):
            errors.append(f"{prefix}.co_speakers: must be an array")
        else:
            for j, person in enumerate(co_speakers):
                if not isinstance(person, str) or not person.strip():
                    errors.append(f"{prefix}.co_speakers[{j}]: must be non-empty string")

        if not isinstance(talk.get("needs_review"), bool):
            errors.append(f"{prefix}.needs_review: must be boolean")

        if isinstance(speaker_id, str) and isinstance(event_year, int) and isinstance(title, str):
            dedupe_key = (speaker_id, event_year, title)
            if dedupe_key in seen_talk_keys:
                errors.append(
                    f"{prefix}: duplicate talk key (speaker_id,event_year,title)={dedupe_key}"
                )
            else:
                seen_talk_keys.add(dedupe_key)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Speaker validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1
    print("Speaker validation passed: data/speakers.json schema is consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
