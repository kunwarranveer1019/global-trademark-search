"""Generate a scoped preliminary trademark research plan."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"
REGISTRY_FILE = DATA_DIR / "sources.json"
SOURCE_REPO_FILE = ROOT / "registries" / "sources.json"
CLASS_FILE = DATA_DIR / "nice_classes_2026.json"


def load_sources() -> list[dict]:
    source_file = REGISTRY_FILE if REGISTRY_FILE.exists() else SOURCE_REPO_FILE
    return json.loads(source_file.read_text(encoding="utf-8"))


def load_classes() -> dict:
    return json.loads(CLASS_FILE.read_text(encoding="utf-8"))


def country_name(code: str) -> str:
    try:
        import pycountry
    except ImportError as exc:
        raise SystemExit("Install project dependencies with `python -m pip install -e .` to use ISO country codes.") from exc
    country = pycountry.countries.get(alpha_2=code)
    if country is None:
        raise SystemExit(f"Unknown ISO 3166-1 alpha-2 country code: {code}")
    return country.name


def directory_source(code: str, name: str) -> dict:
    return {
        "code": code,
        "scope": "national_directory_fallback",
        "name": f"WIPO Country IP Profile — {name}",
        "operator": "World Intellectual Property Organization",
        "search_url": "https://www.wipo.int/en/web/country-profiles/" + code,
        "coverage": "Office discovery only. If this country has a WIPO profile, follow it to the current official national or regional register; otherwise use the WIPO office directory. The profile is not a name-search result and some territories use a regional office.",
        "source_url": "https://www.wipo.int/en/web/country-profiles/directory-ip-offices",
        "directory_fallback_url": "https://www.wipo.int/en/web/country-profiles/directory-ip-offices",
        "query_mode": "locate_official_register_manually"
    }


def select_sources(sources: list[dict], requested: set[str], world: bool) -> list[dict]:
    global_source = next(source for source in sources if source["code"] == "WORLD")
    if not requested and not world:
        return sources
    selected = list(sources) if world else [global_source]
    codes = set(requested)
    if world:
        try:
            import pycountry
        except ImportError as exc:
            raise SystemExit("Install project dependencies with `python -m pip install -e .` to build the worldwide country list.") from exc
        codes.update(country.alpha_2 for country in pycountry.countries)
    for code in sorted(codes):
        matches = [source for source in sources if source["code"] == code]
        if matches:
            if not world:
                selected.extend(matches)
            continue
        selected.append(directory_source(code, country_name(code)))
    deduped = {}
    for source in selected:
        deduped[source["code"]] = source
    return list(deduped.values())


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def score_candidate(name: str, industry: str) -> dict:
    """A transparent naming heuristic, not a registrability/conflict score."""
    n = normalize(name)
    i = set(re.findall(r"[a-z0-9]+", industry.casefold()))
    tokens = set(re.findall(r"[a-z0-9]+", name.casefold()))
    descriptive_overlap = len(tokens & i)
    length_score = max(0, 25 - abs(len(n) - 9) * 3)
    distinctiveness = max(0, 50 - descriptive_overlap * 18)
    pronounceability = 25 if len(n) >= 4 and not re.search(r"[^aeiou]{5}", n) else 10
    return {
        "name": name,
        "heuristic_score": min(100, length_score + distinctiveness + pronounceability),
        "score_meaning": "Name quality heuristic only; not a legal risk or clearance score.",
        "normalized": n,
    }


def candidate_names(seed: str, industry: str) -> list[str]:
    seed_words = re.findall(r"[A-Za-z0-9]+", seed)
    core = seed_words[0].title() if seed_words else "Nova"
    sector = re.findall(r"[A-Za-z0-9]+", industry)
    sector_word = sector[-1].title() if sector else "Works"
    options = [seed, f"{core} & {sector_word}", f"{core}ly", f"{core}ora", f"{core}well",
               f"{core}field", f"{core}kind", f"{core}house", f"{core}wild", f"{core}andCo",
               f"{core}craft", f"{core}root", f"{core}bright", f"{core}north", f"{core}story"]
    seen = set()
    return [x for x in options if normalize(x) and not (normalize(x) in seen or seen.add(normalize(x)))][:10]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a preliminary trademark research plan.")
    parser.add_argument("seed", nargs="?", help="A seed name, concept, or desired brand direction")
    parser.add_argument("--industry", default="", help="Relevant goods/services industry")
    parser.add_argument("--countries", nargs="*", default=[], help="Jurisdiction codes, e.g. US GB EU")
    parser.add_argument("--world", action="store_true", help="Build a source plan for every ISO country/territory")
    parser.add_argument("--classes", nargs="*", default=[], help="Nice class numbers, 1 through 45")
    parser.add_argument("--output", help="Write JSON report to this path")
    parser.add_argument("--list-jurisdictions", action="store_true")
    parser.add_argument("--list-countries", action="store_true", help="List ISO 3166-1 alpha-2 country options")
    parser.add_argument("--list-classes", action="store_true", help="List the 45 Nice classes")
    args = parser.parse_args()
    sources = load_sources()
    if args.list_jurisdictions:
        print(json.dumps(sources, indent=2, ensure_ascii=False))
        return
    if args.list_classes:
        print(json.dumps(load_classes(), indent=2, ensure_ascii=False))
        return
    if args.list_countries:
        try:
            import pycountry
        except ImportError as exc:
            raise SystemExit("Install project dependencies with `python -m pip install -e .` to list ISO country options.") from exc
        countries = [{"code": country.alpha_2, "name": country.name} for country in sorted(pycountry.countries, key=lambda item: item.name)]
        print(json.dumps(countries, indent=2, ensure_ascii=False))
        return
    if not args.seed:
        parser.error("seed is required unless --list-jurisdictions is used")
    requested = {code.upper() for value in args.countries for code in value.split(",") if code}
    requested_world = args.world or bool(requested & {"WORLD", "ALL"})
    requested.discard("WORLD")
    requested.discard("ALL")
    selected = select_sources(sources, requested, requested_world)
    class_catalog = load_classes()
    classes_by_number = {str(item["number"]): item for item in class_catalog["classes"]}
    invalid_classes = [number for number in args.classes if number not in classes_by_number]
    if invalid_classes:
        parser.error("Invalid Nice class number(s): " + ", ".join(invalid_classes) + ". Choose 1 through 45.")
    selected_classes = [classes_by_number[number] for number in args.classes]
    names = [score_candidate(n, args.industry) for n in candidate_names(args.seed, args.industry)]
    names.sort(key=lambda item: (-item["heuristic_score"], item["name"].casefold()))
    for item in names:
        item["search_links"] = [{"source": s["name"], "url": s["search_url"], "search_term_to_enter": item["name"], "query_mode": s["query_mode"]} for s in selected if s["scope"] != "national_directory_fallback"]
        item["search_term_for_directory_fallbacks"] = item["name"]
        item["additional_national_sources_to_discover"] = [s["code"] for s in selected if s["scope"] == "national_directory_fallback"]
        item["review_status"] = "not_searched"
        item["findings"] = [
            {
                "jurisdiction": s["code"],
                "register": s["name"],
                "operator": s.get("operator", ""),
                "status": "not_searched" if s["scope"] != "national_directory_fallback" else "source_discovery_required",
                "indicator": "⚪",
                "query": item["name"],
                "classes": [entry["number"] for entry in selected_classes],
                "checked_at": None,
                "observed_result": "Not inspected; this CLI creates search links/checklists only.",
                "source_url": s.get("search_url"),
                "record_url": None,
                "limitation": s.get("coverage", "Official portal link; live results have not been inspected."),
                "next_action": "Open the official source and search manually; record observed results and direct record links.",
                "manual_verification": {
                    "state": "not_required_or_not_yet_encountered",
                    "resume_rule": "If a human verification check appears, pause this source, let the user complete it directly, then resume only after explicit confirmation and inspectable result evidence. Never automate or bypass the check."
                }
            }
            for s in selected
        ]
    report = {
        "product": "MarkScout", "report_type": "preliminary_trademark_research_plan",
        "created_at": datetime.now(timezone.utc).isoformat(), "seed": args.seed,
        "industry": args.industry, "jurisdictions_requested": "world_all_iso_codes" if requested_world else (sorted(requested) if requested else "all_configured_sources_default"),
        "coverage_note": "Country codes are ISO 3166-1 alpha-2. In world mode the source list includes configured national portals plus a WIPO profile for each ISO country/territory without a configured portal; those profile links are office-discovery steps, not completed searches. All live registry searches remain subject to each portal's access rules and coverage limits.",
        "nice_classification": {"edition": class_catalog["edition"], "effective_date": class_catalog["effective_date"], "source": class_catalog["source"], "selected_classes": selected_classes, "available_classes": class_catalog["classes"], "local_adoption_note": class_catalog["notes"]},
        "sources": selected, "candidates": names,
        "findings_table": {
            "required": True,
            "columns": ["candidate", "jurisdiction/register", "status", "query_and_filters", "nice_classes", "checked_at", "observed_result", "official_source_or_record_url", "limitations", "next_action"],
            "legend": [
                {"indicator": "🟢", "status": "no_relevant_record_observed", "meaning": "An inspected query returned no relevant record; this is not clearance."},
                {"indicator": "🟡", "status": "possible_match_or_partial_or_manual_follow_up", "meaning": "Possible similarity, partial search, or further human review is needed."},
                {"indicator": "🔴", "status": "potentially_relevant_record", "meaning": "A potentially relevant record was observed; link it and explain the basis."},
                {"indicator": "⚪", "status": "not_searched_or_awaiting_verification_or_results_unavailable", "meaning": "No live result evidence was inspected; state why and the next step."}
            ],
            "completeness_rule": "Include one row for every candidate, selected jurisdiction, and relevant source, including no-result, pending, blocked, and unsearched rows. Pair emoji with text labels for accessibility."
        },
        "manual_verification_workflow": {
            "on_challenge": "Pause this source and present/open its official URL, query, and manual steps. Continue independent sources.",
            "user_action": "The user completes the official check directly with the source.",
            "resume_condition": "Resume only after the user explicitly confirms completion or supplies result records; inspect only results available in the authorized session or user-provided evidence.",
            "unavailable_session": "Request result text/export/direct record links and keep status manual_results_not_provided until then.",
            "prohibited": ["CAPTCHA solving", "automating verification", "proxying around verification", "storing CAPTCHA answers or session tokens"],
            "checkpoint_fields": ["jurisdiction", "official_url", "candidate", "query", "classes", "last_completed_step", "handoff_time", "status"]
        },
        "logo_guidance": "Copyright originality and trademark similarity are different questions. Search logo/device marks in each source's official image or Vienna-code search when available. Similarity tools require human review and cannot certify freedom to use.",
        "access_policy": "Use public interfaces according to their terms. If CAPTCHA, login, rate-limit, or human verification appears, pause that source, hand off the official link for direct user completion, and resume only after explicit confirmation plus inspectable evidence. Never bypass it.",
        "legal_note": "No candidate is certified available or copyright-free. Obtain qualified trademark counsel review before adoption or filing."
    }
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
