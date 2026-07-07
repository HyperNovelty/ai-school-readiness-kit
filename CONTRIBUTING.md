# Contributing

Contributions should keep the kit practical, plain-spoken, and usable by local school communities.

Use synthetic examples only. Do not add real student data, school names, private cases, account data, unpublished materials, or private source traces. Avoid claims that sound like legal, compliance, medical, or mental-health advice.

Preferred changes include clearer checklist language, better local review prompts, stronger examples, and small improvements to the validator or renderer that keep the project Python standard library only.

Before considering a change complete, run:

```bash
python3 scripts/validate_readiness_card.py examples/school-ai-readiness-card.example.json
python3 scripts/render_readiness_card_html.py examples/school-ai-readiness-card.example.json examples/rendered/school-ai-readiness-card.example.html
python3 -m unittest discover -s tests
git diff --check
```
