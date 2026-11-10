# Integration policy and current capability

## Current behavior

The CLI creates an evidence checklist and direct official search-page links. It does not submit forms, collect results, or claim a registry was searched. The AI skill tells a connected model to inspect each source and record only observed results. This is deliberate: search portals have different coverage, languages, status fields, and access requirements.

## API integration rules

An API should be added only when its official documentation confirms that it supports the required name/mark search, its permitted use and authentication are understood, and the returned fields include enough context to cite the result. A case-status or document API is not a substitute for a name-search API. A portal URL with an invented query parameter is not a verified integration.

For every future adapter:

1. Link the official API documentation and terms.
2. Identify which search modes it supports (exact, fuzzy, phonetic, goods/services, image/device) and what it omits.
3. Store credentials outside the repository and redact them from reports/logs.
4. Respect rate limits, access controls, robots/terms and personal-data rules.
5. Stop and hand off when the source requires a CAPTCHA, login, or human verification. Never bypass that gate.
6. Preserve source, jurisdiction, query, timestamp, record URL, status, class, and a source limitation with each result.

## Known official sources

- WIPO Global Brand Database is a multi-collection discovery portal. WIPO recommends checking national or regional registers as well.
- EUIPO Search IP links to TMview, which covers participating offices; it is not worldwide coverage.
- USPTO Trademark Search is the official US name-search portal. USPTO's documented TSDR API supports record/status/document access and requires an API key; do not treat it as the name-search interface.
- UK IPO, CIPO, IP Australia, IP India, J-PlatPat, INPI Brazil, KIPRIS, IPOS Digital Hub, and CNIPA are configured as official national search portals. Query terms are supplied beside the link for manual entry; some portals require local-language search variants.

Review each source's documentation and terms again before changing this capability. Registry interfaces and API access can change.
