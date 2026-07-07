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

## How To Validate A Card

From the repository root:

```bash
python3 scripts/validate_readiness_card.py examples/school-ai-readiness-card.example.json
```

The validator checks required fields, simple field types, allowed review status values, and the local readiness rule:

If `student_data_involved` is true, `human_review_steps` must include at least one item and `family_communication_needed` must be true.

## How To Render A Review Page

```bash
python3 scripts/render_readiness_card_html.py examples/school-ai-readiness-card.example.json /tmp/school-ai-readiness-card.html
```

Open the generated HTML file in a browser, including on Windows. The renderer uses Python standard library only and escapes card content before writing HTML.

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

