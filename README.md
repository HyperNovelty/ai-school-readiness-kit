# AI School Readiness Kit

AI School Readiness Kit is a local-only starter kit for reviewing proposed AI use in school and learning-program settings before it affects assignments, assessment, privacy, access, or student trust.

It is built for teachers, parents, school leaders, tutors, library programs, after-school programs, and community learning groups that need a practical checklist before using an AI tool with students.

This kit is part of the Hypernovelty Open Lab footprint. It coordinates with the public `education-adaptation-cards` project, but it does not duplicate that deck or replace it:

https://github.com/HyperNovelty/education-adaptation-cards

Use this repository for local readiness review. Use the adaptation cards as a public conversation and scenario resource.

## What Is Here

- Field guidance for reviewing classroom AI use.
- Plain checklists for classroom use, assignment review, and student privacy.
- A small readiness-card JSON schema.
- A validator for readiness cards.
- A local HTML renderer for a readable review page.
- Synthetic examples only.

## What This Helps With

The kit helps a local reviewer ask:

- What school context is involved?
- Who is affected by the AI use?
- Is student data involved?
- Could assessment, grading, feedback, or placement be affected?
- What human review is required?
- Is family communication needed?
- What should this AI use explicitly not be used for?

## School/Admin Quick Start

1. Review `docs/field-guide.md`.
2. Use `docs/reviewer-route-admin-teacher-family.md` to gather administrator, teacher, and family questions.
3. Pick the closest checklist in `kits/`.
4. Copy `examples/school-ai-readiness-card.example.json` and replace it with synthetic or locally approved public-safe details.
5. Mark sensitive, assessment-impacting, surveillance, discipline, counseling, health, or regulated uses as `needs_policy_review` or `do_not_use`.
6. Validate and render the card before local discussion.

## How To Validate A Card

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_readiness_card.py examples/school-ai-readiness-card.example.json
```

The validator checks required fields, simple field types, allowed review status values, and the local readiness rule:

If `student_data_involved` is true, `human_review_steps` must include at least one item and `family_communication_needed` must be true.

## How To Render A Review Page

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/render_readiness_card_html.py examples/school-ai-readiness-card.example.json examples/rendered/school-ai-readiness-card.example.html
```

Open `examples/rendered/school-ai-readiness-card.example.html` in a browser, including on Windows. The renderer uses Python standard library only and escapes card content before writing HTML.

Run tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

## What This Repo Does Not Do

This repository does not provide legal, compliance, medical, or mental-health advice. It does not authorize policy decisions. It does not store student data. It does not call external APIs. It does not connect to school systems, learning platforms, gradebooks, identity providers, or AI services.

It is a local review aid for sober, practical, public-good use.

## Boundaries

- Local files only.
- Synthetic examples only.
- No real student data.
- No school names or private cases.
- No external APIs.
- No account tools.
- No policy authorization.
- No legal, compliance, medical, or mental-health claims.

For distinct administrator, teacher, and family prompts, see `docs/reviewer-route-admin-teacher-family.md`.

## Open Lab Fit

This repo is part of the Hypernovelty Open Lab public proof footprint. See `docs/open-lab-positioning.md` for how school readiness review connects to the umbrella kit, verification literacy labs, source cards, workflow screens, and agent receipts.
