# MarkScout

MarkScout is a portable AI plugin and Python starter kit for **preliminary trademark clearance**. It helps teams define markets and industry classes, search official or institution-run trademark portals, compare candidate names, and generate an evidence-backed shortlist.

> Brand names and logos are usually assessed as trademarks; copyright protects original creative expression. A search cannot certify a name or logo as “copyright-free,” available, or legally safe. This tool reports only what its cited sources show and when they were checked.

## What is included

- A portable Agent Plugins package in `plugin/` with a reusable skill for ChatGPT, Codex, and compatible AI clients.
- `prompts/clearance-workflow.md`, a detailed model-agnostic prompt.
- A Python CLI that produces candidate names, applies transparent similarity heuristics, and generates official search links for selected jurisdictions.
- A registry directory that can be extended with verified government/institution portals.
- Explicit source, coverage, date, and manual-review reporting; no CAPTCHA bypass, stealth browser automation, or evasion of access controls.

## Quick start

Requires Python 3.10+ and `pycountry` for ISO country options. From the repository root, install the package first:

```bash
python -m pip install -e .
python -m markscout "Lumen Grove" --industry "sustainable skincare" --countries US GB EU --classes 3 35 --output report.json
```

Use `--world` to build a source plan for every ISO country/territory, `--list-jurisdictions` to inspect curated coverage, `--list-countries` to list all ISO 3166-1 alpha-2 options, and `--list-classes` to list all 45 Nice classes. `--countries` accepts multiple codes separated by spaces or commas. For a valid country code without a curated national portal, the report includes its WIPO country profile and directory fallback to locate the official IP office. The CLI does not scrape portal results or assert that a candidate is clear. It creates a structured checklist and official search links so a researcher or connected AI/browser can inspect live records under each portal's terms.

## Coverage model

This starter version has entry points for WIPO Global Brand Database, EUIPO/TMview, and national portals in the US, UK, Canada, Australia, India, Japan, Brazil, South Korea, Singapore, and China. Any ISO alpha-2 country can be selected, with WIPO country-profile fallback for countries not yet curated. The WIPO Nice Classification selector includes 45 classes from NCL 13-2026; confirm local adoption and exact goods/services terms at each office. Aggregators do not replace national registers. “World” builds a source plan for all ISO countries/territories, using configured national portals where available and WIPO profiles to find other national or regional offices. It does not perform comprehensive live searches of every register. Portal links open official search pages and the report supplies the candidate term to enter; the CLI does not guess undocumented query URL formats. See `registries/README.md` and `registries/INTEGRATION_POLICY.md`.

## Development

```bash
python -m markscout --list-countries
python -m markscout --list-classes
python -m markscout "Northstar Pantry" --industry "food retail" --countries US GB --classes 29 30 35
```

Registry source data is maintained in `registries/sources.json` and bundled under `markscout/data/sources.json`; run `python scripts/sync_registry_sources.py` after editing the source directory. Classification data is bundled with the package. The implementation uses the Python standard library plus `pycountry` for ISO country names/codes.

## Safety and data handling

Search operates only through public, authorized interfaces. If a site presents a CAPTCHA, login, rate limit, or other human-verification step, stop automated interaction and provide the official link for a person to continue. Do not store applicant personal data unnecessarily. Never present heuristic name scores as legal opinions.

## Repository layout

```text
plugin/       Portable plugin package to install or upload
markscout/    Python CLI and scoring utilities
registries/   Source directory and coverage notes
prompts/      Detailed model-agnostic workflow prompt
```

## License

MIT; see `LICENSE`.
