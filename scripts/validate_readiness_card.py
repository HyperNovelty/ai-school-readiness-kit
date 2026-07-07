#!/usr/bin/env python3
"""Validate a school AI readiness card using Python standard library only."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "card_id": str,
    "title": str,
    "school_context": str,
    "audience": str,
    "ai_use_case": str,
    "student_data_involved": bool,
    "assessment_impact": str,
    "equity_access_notes": list,
    "human_review_steps": list,
    "family_communication_needed": bool,
    "not_for": list,
    "review_status": str,
}

ARRAY_STRING_FIELDS = {"equity_access_notes", "human_review_steps", "not_for"}
ALLOWED_REVIEW_STATUS = {
    "draft",
    "ready_for_local_review",
    "needs_policy_review",
    "do_not_use",
}


def load_card(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("card must be a JSON object")
    return data


def validate_card(card: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in card:
            errors.append(f"missing required field: {field}")
            continue
        if not isinstance(card[field], expected_type):
            errors.append(f"{field} must be {expected_type.__name__}")

    extra_fields = sorted(set(card) - set(REQUIRED_FIELDS))
    for field in extra_fields:
        errors.append(f"unexpected field: {field}")

    for field in ARRAY_STRING_FIELDS:
        value = card.get(field)
        if isinstance(value, list):
            for index, item in enumerate(value):
                if not isinstance(item, str):
                    errors.append(f"{field}[{index}] must be str")

    review_status = card.get("review_status")
    if isinstance(review_status, str) and review_status not in ALLOWED_REVIEW_STATUS:
        allowed = ", ".join(sorted(ALLOWED_REVIEW_STATUS))
        errors.append(f"review_status must be one of: {allowed}")

    if card.get("student_data_involved") is True:
        steps = card.get("human_review_steps")
        if not isinstance(steps, list) or len(steps) == 0:
            errors.append(
                "student_data_involved requires at least one human_review_steps item"
            )
        if card.get("family_communication_needed") is not True:
            errors.append(
                "student_data_involved requires family_communication_needed to be true"
            )

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_readiness_card.py CARD.json", file=sys.stderr)
        return 2

    path = Path(argv[1])
    try:
        card = load_card(path)
        errors = validate_card(card)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"invalid: {error}", file=sys.stderr)
        return 1

    print(f"valid: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

