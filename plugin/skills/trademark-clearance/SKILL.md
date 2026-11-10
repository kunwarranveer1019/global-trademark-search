---
name: trademark-clearance
description: Use when researching a brand name or logo against official trademark registries, selecting jurisdictions, generating industry-related name ideas, or explaining preliminary clearance limits.
---

# Preliminary trademark clearance workflow

Follow `references/clearance-workflow.md` for the complete intake, registry search, candidate ranking, logo review, and output process. Use `references/official-sources.md` as the starter directory of official portals and their coverage notes.

## Core behavior

- Clarify industry, goods/services, relevant markets, languages, and whether the user wants word marks, logos, or both. Support multiple ISO alpha-2 jurisdictions and a “World” source-plan option that includes all ISO codes.
- Accept any ISO 3166-1 alpha-2 country code. In World mode, include every ISO country/territory. Use configured national portal links where available; otherwise use the matching WIPO country profile or office directory to locate the current official IP office and its register. Never imply that a WIPO profile itself performed a name search.
- Offer all 45 Nice classes from NCL 13-2026. Ask about the user's goods/services, allow multiple class selections, and confirm whether each office follows the same class wording or has local requirements. See `references/nice-classes-2026.json` and its official WIPO source.
- Prefer official national or regional IP office registers. WIPO Global Brand Database and EUIPO/TMview are discovery sources; aggregated databases may be incomplete, so search national registers in the actual target markets.
- Generate at least 10 tailored names when requested. Separate brand-fit ranking from search evidence. Record exact/phonetic/visual variants, goods/services classes, source, date, query, status, and direct links.
- For logo requests, propose original concepts and check device/image marks only where official tools support it. Never claim artwork or names are “copyright-free” or guaranteed clear.
- Do not say a source was searched if results were not inspected. Mark each unsearched source and explain why.
- If a portal requires a CAPTCHA, login, rate-limit wait, or human verification, stop automation. Give the user the official link and manual steps; never bypass or defeat the check.
- Distinguish facts from inference. A zero-result query is not clearance. Recommend qualified trademark counsel before adoption or filing.

The supporting workflow prompt is in `references/clearance-workflow.md`.
