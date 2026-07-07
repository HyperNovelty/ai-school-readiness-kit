#!/usr/bin/env python3
"""Render a school AI readiness card as a local HTML review page."""

from __future__ import annotations

import html
import sys
from pathlib import Path

try:
    from validate_readiness_card import load_card, validate_card
except ModuleNotFoundError:
    from scripts.validate_readiness_card import load_card, validate_card


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_list(items: list[str]) -> str:
    if not items:
        return "<p>None listed.</p>"
    entries = "\n".join(f"      <li>{esc(item)}</li>" for item in items)
    return f"<ul>\n{entries}\n    </ul>"


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def render_card_html(card: dict[str, object]) -> str:
    title = esc(card["title"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.5; margin: 2rem; max-width: 920px; color: #222; }}
    header {{ border-bottom: 2px solid #333; margin-bottom: 1.5rem; }}
    h1, h2 {{ line-height: 1.2; }}
    dl {{ display: grid; grid-template-columns: minmax(180px, 260px) 1fr; gap: 0.5rem 1rem; }}
    dt {{ font-weight: bold; }}
    dd {{ margin: 0; }}
    section {{ margin: 1.5rem 0; }}
    .status {{ display: inline-block; border: 1px solid #555; padding: 0.25rem 0.5rem; }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p class="status">Review status: {esc(card["review_status"])}</p>
  </header>
  <main>
    <section>
      <h2>Summary</h2>
      <dl>
        <dt>Card ID</dt><dd>{esc(card["card_id"])}</dd>
        <dt>School context</dt><dd>{esc(card["school_context"])}</dd>
        <dt>Audience</dt><dd>{esc(card["audience"])}</dd>
        <dt>AI use case</dt><dd>{esc(card["ai_use_case"])}</dd>
        <dt>Student data involved</dt><dd>{yes_no(bool(card["student_data_involved"]))}</dd>
        <dt>Family communication needed</dt><dd>{yes_no(bool(card["family_communication_needed"]))}</dd>
        <dt>Assessment impact</dt><dd>{esc(card["assessment_impact"])}</dd>
      </dl>
    </section>
    <section>
      <h2>Equity and Access Notes</h2>
      {render_list(card["equity_access_notes"])}
    </section>
    <section>
      <h2>Human Review Steps</h2>
      {render_list(card["human_review_steps"])}
    </section>
    <section>
      <h2>Not For</h2>
      {render_list(card["not_for"])}
    </section>
  </main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: render_readiness_card_html.py CARD.json OUT.html", file=sys.stderr)
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    try:
        card = load_card(input_path)
        errors = validate_card(card)
    except Exception as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"invalid: {error}", file=sys.stderr)
        return 1

    output_path.write_text(render_card_html(card), encoding="utf-8")
    print(f"rendered: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
