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
- If a portal requires a CAPTCHA, login, rate-limit wait, or human verification, pause that source and open/provide its official URL in the browser. Show the exact query and manual steps. Do not solve, automate, proxy around, or otherwise bypass the check. Keep the source marked `awaiting_manual_verification`; continue other independently accessible sources. Resume that source only after the user explicitly confirms they completed the check (or provides the resulting records). Then inspect only results the user has made available through the authorized session and record the exact observed evidence. If the portal session cannot be resumed or exposed to the model, ask the user to paste/export the results and keep it marked `manual_results_not_provided` until then. Never claim that CAPTCHA completion alone means a search completed.
- Present all findings in a complete Markdown table with a status word and colour indicator: 🟢 no relevant record observed in the inspected query (not clearance); 🟡 possible/uncertain match, partial search, or manual follow-up; 🔴 potentially relevant conflicting record observed; ⚪ not searched or no result evidence. Use text labels alongside emoji so colour is not the only signal. Include a row for every candidate × jurisdiction/source searched or planned, plus source URL, query, classes, check date, evidence/record links, limitations, and next action. Summarize counts, but do not omit rows for “no results” or incomplete sources.
- Distinguish facts from inference. A zero-result query is not clearance. Recommend qualified trademark counsel before adoption or filing.

The supporting workflow prompt is in `references/clearance-workflow.md`.
