"""Structural eval harness for leverage-os audit outputs.

Runs each audit against fixture personas, checks structural conformance
(required headers, table shape, field constraints), and optionally measures
determinism overlap between paired runs.

Usage:
    python -m leverage_os.evals                   # manual provider (no API calls)
    python -m leverage_os.evals --provider bedrock # real LLM, costs ~$0.20/fixture
    python -m leverage_os.evals --determinism     # run twice, measure overlap
"""

import json
import os
import re
import sys
from pathlib import Path

from .prompts import AUDIT_MAP, ALL_AUDITS
from .runner import get_provider

FIXTURES_DIR = Path(__file__).parent.parent / "tests" / "fixtures"
STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "to", "of", "in", "for",
             "and", "or", "but", "with", "on", "at", "by", "from", "that", "this",
             "it", "i", "my", "you", "your"}


def load_fixtures() -> list[dict]:
    fixtures = []
    for f in sorted(FIXTURES_DIR.glob("answers_*.json")):
        fixtures.append(json.loads(f.read_text()))
    return fixtures


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-z]+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}


def overlap_ratio(a: str, b: str) -> float:
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def find_header(text: str, header: str) -> bool:
    return f"**{header}**" in text or f"**{header}:**" in text


def count_table_rows(text: str, after_header: str) -> int:
    idx = text.find(f"**{after_header}")
    if idx == -1:
        return 0
    chunk = text[idx:]
    rows = re.findall(r"^\|(?!\s*[-:])[^|]+\|.+\|$", chunk, re.MULTILINE)
    return max(0, len(rows) - 1)


def count_table_cols(text: str, after_header: str) -> int:
    idx = text.find(f"**{after_header}")
    if idx == -1:
        return 0
    chunk = text[idx:]
    header_row = re.search(r"^\|(.+)\|$", chunk, re.MULTILINE)
    if not header_row:
        return 0
    return len(header_row.group(1).split("|"))


def eval_knowledge(text: str) -> list[tuple[str, bool]]:
    results = []
    results.append(("Has 'Your Specific Knowledge Niche' header", find_header(text, "Your Specific Knowledge Niche:")))
    results.append(("Has 'Why This is Rare' header", find_header(text, "Why This is Rare:")))
    results.append(("Has '3 Leveraged Business Models' header", find_header(text, "3 Leveraged Business Models:")))
    results.append(("Table has 6 columns", count_table_cols(text, "3 Leveraged Business Models:") == 6))
    results.append(("Table has 3 data rows", count_table_rows(text, "3 Leveraged Business Models:") == 3))
    results.append(("Has 'Recommended Starting Point' header", find_header(text, "Recommended Starting Point:")))
    results.append(("No 'labor' in leverage types", "labor" not in text.lower().split("leverage type")[1][:200] if "leverage type" in text.lower() else True))
    return results


def eval_leverage(text: str) -> list[tuple[str, bool]]:
    results = []
    results.append(("Has 'Leverage Audit' header", find_header(text, "Leverage Audit:")))
    results.append(("Table has 5 columns", count_table_cols(text, "Leverage Audit:") == 5))
    results.append(("Table has ≥1 data row", count_table_rows(text, "Leverage Audit:") >= 1))
    results.append(("Has 'Your Leverage Index' header", find_header(text, "Your Leverage Index:")))
    idx_match = re.search(r"\*\*Your Leverage Index:\*\*\s*(\d+\.?\d*)/5", text)
    results.append(("Leverage Index is X/5 format", idx_match is not None))
    results.append(("Has 'Biggest Leverage Leak' header", find_header(text, "Biggest Leverage Leak:")))
    results.append(("Has '3 Upgrade Moves' header", find_header(text, "3 Upgrade Moves:")))
    results.append(("Has '30 Day First Move' header", find_header(text, "30 Day First Move:")))
    return results


def eval_productize(text: str) -> list[tuple[str, bool]]:
    results = []
    results.append(("Has 'Your Core Transformation' header", find_header(text, "Your Core Transformation:")))
    results.append(("Transformation has 'I help' pattern", "i help" in text.lower()[:text.lower().find("3 product") if "3 product" in text.lower() else 500]))
    results.append(("Has '3 Product Formats' header", find_header(text, "3 Product Formats:")))
    results.append(("Table has 5 columns", count_table_cols(text, "3 Product Formats:") == 5))
    results.append(("Table has 3 data rows", count_table_rows(text, "3 Product Formats:") == 3))
    results.append(("Has 'Winning Product Structure' header", find_header(text, "Winning Product Structure:")))
    results.append(("Has 'Name:' field", "Name:" in text or "name:" in text))
    results.append(("Has 'Launch Positioning' header", find_header(text, "Launch Positioning:")))
    results.append(("Has 'Week 1 Roadmap' header", find_header(text, "Week 1 Roadmap:")))
    return results


def eval_time_leak(text: str) -> list[tuple[str, bool]]:
    results = []
    results.append(("Has 'Time Audit' header", find_header(text, "Time Audit:")))
    results.append(("Table has 5 columns", count_table_cols(text, "Time Audit:") == 5))
    results.append(("Table has ≥1 data row", count_table_rows(text, "Time Audit:") >= 1))
    results.append(("Has 'Your Time Rent Ratio' header", find_header(text, "Your Time Rent Ratio:")))
    ratio_match = re.search(r"(\d+)%\s*rented\s*/\s*(\d+)%\s*equity", text)
    results.append(("Ratio format X% rented / Y% equity", ratio_match is not None))
    if ratio_match:
        results.append(("Ratio sums to ~100%", abs(int(ratio_match.group(1)) + int(ratio_match.group(2)) - 100) <= 1))
    results.append(("Has 'Top 3 Conversion Opportunities' header", find_header(text, "Top 3 Conversion Opportunities:")))
    results.append(("Has 'The Equity Gap' header", find_header(text, "The Equity Gap:")))
    results.append(("Has 'First Escape Move' header", find_header(text, "First Escape Move:")))
    return results


EVAL_FNS = {
    "knowledge": eval_knowledge,
    "leverage": eval_leverage,
    "productize": eval_productize,
    "time_leak": eval_time_leak,
}


def run_evals(provider_name: str = "manual", determinism: bool = False):
    fixtures = load_fixtures()
    if not fixtures:
        print("No fixtures found in tests/fixtures/. Exiting.")
        sys.exit(1)

    provider = get_provider(provider_name)
    print(f"Provider: {provider.name} | Fixtures: {len(fixtures)} | Audits: {len(ALL_AUDITS)}")
    print("=" * 70)

    total_checks = 0
    total_passed = 0
    all_outputs: dict[str, dict[str, list[str]]] = {}

    for fixture in fixtures:
        persona = fixture["persona"]
        answers = fixture["answers"]
        print(f"\n--- Persona: {persona} ---")
        all_outputs[persona] = {}

        for audit_key in ALL_AUDITS:
            title, builder = AUDIT_MAP[audit_key]
            prompt = builder(answers)
            response = provider.invoke(prompt)

            if response is None:
                if provider_name == "manual":
                    print(f"  [{audit_key}] SKIP (manual provider returns None — use --provider bedrock for real eval)")
                    continue
                print(f"  [{audit_key}] FAIL — provider returned None")
                continue

            runs = [response]
            if determinism:
                second = provider.invoke(prompt)
                if second:
                    runs.append(second)

            all_outputs[persona].setdefault(audit_key, []).extend(runs)

            eval_fn = EVAL_FNS[audit_key]
            checks = eval_fn(response)
            passed = sum(1 for _, ok in checks if ok)
            total_checks += len(checks)
            total_passed += passed

            status = "PASS" if passed == len(checks) else "PARTIAL"
            print(f"  [{audit_key}] {status} ({passed}/{len(checks)})")
            for label, ok in checks:
                if not ok:
                    print(f"    FAIL: {label}")

    print("\n" + "=" * 70)
    if total_checks > 0:
        print(f"Total: {total_passed}/{total_checks} checks passed ({100*total_passed//total_checks}%)")
    else:
        print("No checks run (manual provider skips all). Use --provider bedrock.")

    if determinism and provider_name != "manual":
        print("\n--- Determinism overlap ---")
        for persona, audits in all_outputs.items():
            for audit_key, runs in audits.items():
                if len(runs) >= 2:
                    ratio = overlap_ratio(runs[0], runs[1])
                    print(f"  {persona}/{audit_key}: {ratio:.2f} Jaccard overlap")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Structural eval harness for leverage-os")
    parser.add_argument("--provider", default="manual", help="LLM provider (manual, bedrock)")
    parser.add_argument("--determinism", action="store_true", help="Run each audit twice and measure overlap")
    args = parser.parse_args()
    run_evals(provider_name=args.provider, determinism=args.determinism)


if __name__ == "__main__":
    main()
