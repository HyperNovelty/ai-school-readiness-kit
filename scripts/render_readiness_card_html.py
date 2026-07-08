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
        return '<p class="empty">None listed.</p>'
    entries = "\n".join(f"      <li>{esc(item)}</li>" for item in items)
    return f'<ul class="check-list">\n{entries}\n    </ul>'


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
    :root {{ color-scheme: dark; --ink: #f7ead7; --muted: #d7c2a2; --paper: #fff7e8; --paper-ink: #261b12; --line: #6f5840; --accent: #f2b66d; --warn: #ffd08a; }}
    * {{ box-sizing: border-box; }}
    body {{ color: var(--ink); font-family: Georgia, "Times New Roman", serif; line-height: 1.6; margin: 0; background: #20150f; }}
    body::before {{ content: ""; position: fixed; inset: 0; pointer-events: none; background: radial-gradient(circle at top left, rgba(242, 182, 109, 0.16), transparent 34rem); }}
    .page {{ max-width: 1080px; margin: 0 auto; padding: 32px 18px 44px; position: relative; }}
    header {{ border: 1px solid var(--line); border-radius: 8px; margin-bottom: 18px; padding: 24px; background: linear-gradient(135deg, #3a2617, #251810); box-shadow: 0 18px 50px rgba(0,0,0,0.25); }}
    h1 {{ color: var(--ink); font-size: clamp(2rem, 5vw, 4rem); line-height: 0.98; margin: 10px 0 14px; letter-spacing: 0; }}
    h2 {{ color: var(--paper-ink); font-size: 1.02rem; line-height: 1.2; margin: 0 0 10px; }}
    p {{ margin: 0; }}
    section, .meta-card {{ background: var(--paper); border: 1px solid #dfcaa8; border-radius: 8px; color: var(--paper-ink); padding: 18px; }}
    .eyebrow {{ color: var(--accent); font-family: Arial, Helvetica, sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .status, .chip {{ border: 1px solid rgba(255,255,255,0.28); border-radius: 999px; color: var(--ink); display: inline-flex; font-family: Arial, Helvetica, sans-serif; font-size: 0.78rem; font-weight: 700; padding: 6px 10px; }}
    .status {{ background: rgba(255, 208, 138, 0.18); color: #ffe2ac; }}
    .chip {{ background: rgba(255,255,255,0.08); }}
    dl.summary {{ display: grid; gap: 10px 14px; grid-template-columns: minmax(180px, 260px) 1fr; }}
    dt {{ color: #735230; font-family: Arial, Helvetica, sans-serif; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }}
    dd {{ margin: 0; }}
    main {{ display: grid; gap: 14px; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    main section.wide {{ grid-column: 1 / -1; }}
    .check-list {{ margin: 0; padding-left: 1.2rem; }}
    .check-list li {{ margin: 0.45rem 0; padding-left: 0.15rem; }}
    .empty {{ color: #7a6a55; font-style: italic; }}
    footer {{ color: var(--muted); font-family: Arial, Helvetica, sans-serif; font-size: 0.9rem; margin-top: 18px; }}
    @media (max-width: 760px) {{ main, dl.summary {{ grid-template-columns: 1fr; }} header {{ padding: 20px; }} }}
    @media print {{ body {{ background: #fff; color: #000; }} body::before {{ display: none; }} .page {{ max-width: none; padding: 0; }} header, section {{ box-shadow: none; break-inside: avoid; }} }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <p class="eyebrow">Hypernovelty Open Lab / School AI Readiness Card</p>
      <h1>{title}</h1>
      <div class="chips" aria-label="Readiness status">
        <span class="status">Review status: {esc(card["review_status"])}</span>
        <span class="chip">Synthetic example</span>
        <span class="chip">Human review required</span>
      </div>
    </header>
  <main>
    <section class="wide">
      <h2>Summary</h2>
      <dl class="summary">
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
  <footer>This readiness card is a local synthetic review aid for discussion. It is not legal, student safety, procurement, deployment, or policy approval advice.</footer>
  </div>
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
