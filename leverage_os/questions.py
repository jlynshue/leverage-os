"""Consolidated intake questions for all four audit frameworks."""

import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

QUESTIONS = {
    # Shared / Knowledge Excavator
    "obsessions": {
        "prompt": "What are your obsessions — things you read about unpaid? (list 3-5, comma-separated)",
        "used_by": ["knowledge", "productize"],
    },
    "career_path": {
        "prompt": "Describe your weird career path in 2-3 sentences:",
        "used_by": ["knowledge"],
    },
    "undervalued_skills": {
        "prompt": "Skills others compliment that you don't think are special? (list 2-3, comma-separated)",
        "used_by": ["knowledge"],
    },
    # Leverage Stack Auditor
    "income_sources": {
        "prompt": "List your income sources with hours/week and revenue % for each:\n  (e.g., 'Consulting: 20hrs/wk, 60% | SaaS product: 5hrs/wk, 25% | Investments: 1hr/wk, 15%')",
        "used_by": ["leverage", "time_leak"],
    },
    "monthly_income_target": {
        "prompt": "What is your monthly income target? (e.g., $15,000)",
        "used_by": ["leverage"],
    },
    "skills_assets": {
        "prompt": "What are your main skills or assets you own? (comma-separated)",
        "used_by": ["leverage"],
    },
    # Productize Yourself Blueprint
    "expertise_transformation": {
        "prompt": "What expertise/transformation do you provide? (What do you help people do or become?)",
        "used_by": ["productize"],
    },
    "platforms_audiences": {
        "prompt": "What are your current platforms or audiences? (list them, even if small or none)",
        "used_by": ["productize"],
    },
    "hours_available": {
        "prompt": "How many hours per week do you have available to build? (e.g., 10)",
        "used_by": ["productize"],
    },
    # Time-for-Money Leak Detector
    "work_activities": {
        "prompt": "Describe your work activities and how you're compensated for each:\n  (e.g., 'Client consulting - hourly rate | Product dev - equity | Content - ad revenue')",
        "used_by": ["time_leak"],
    },
    "total_hours_weekly": {
        "prompt": "Total hours worked per week? (e.g., 45)",
        "used_by": ["time_leak"],
    },
    "current_monthly_income": {
        "prompt": "Current monthly income? (e.g., $12,000)",
        "used_by": ["time_leak"],
    },
    "income_split": {
        "prompt": "Income split — active vs passive? (e.g., 80% / 20%)",
        "used_by": ["time_leak"],
    },
}


def collect_answers(audit_filter: str | None = None) -> dict[str, str]:
    """Collect answers interactively. Optionally filter to questions for a specific audit."""
    console.print(
        Panel(
            "[bold cyan]Welcome to Leverage OS[/bold cyan]\n"
            "Naval Ravikant-style self-audit powered by AI\n\n"
            "Answer these questions once — they'll be used across all analyses.",
            title="🔍 Leverage OS",
            border_style="cyan",
        )
    )
    console.print()

    answers = {}

    for key, q in QUESTIONS.items():
        # If filtering to a specific audit, skip irrelevant questions
        if audit_filter and audit_filter not in q["used_by"]:
            continue

        answer = questionary.text(
            q["prompt"],
            multiline="\n" in q["prompt"],
        ).ask()

        if answer is None:
            # User cancelled
            console.print("[red]Cancelled.[/red]")
            raise SystemExit(1)

        answers[key] = answer.strip()
        console.print()

    return answers
