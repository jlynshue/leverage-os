"""Output module — saves results as markdown files + structured run records."""

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console

console = Console()


def _generate_run_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    short = uuid.uuid4().hex[:4]
    return f"{ts}-{short}"


def _hash_answers(answers: dict) -> str:
    raw = json.dumps(answers, sort_keys=True)
    return f"sha256:{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


def save_run_record(
    run_id: str,
    audits_run: list[str],
    provider_name: str,
    model: str,
    answers: dict,
    output_path: str,
    opportunities_extracted: int = 0,
    output_dir: str = "./outputs",
) -> str:
    """Persist a structured JSON run record per SCAFFOLDING.md §5.1."""
    runs_dir = Path(output_dir) / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "audits_run": audits_run,
        "provider": provider_name,
        "model": model,
        "prompt_framework_version": "0.1.0",
        "answers_hash": _hash_answers(answers),
        "output_path": output_path,
        "opportunities_extracted": opportunities_extracted,
        "notes": "",
    }

    filepath = runs_dir / f"{run_id}.json"
    filepath.write_text(json.dumps(record, indent=2) + "\n")
    return str(filepath)


def save_results(results: dict[str, str], output_dir: str = "./outputs") -> str:
    """Save all audit results to a single markdown file.
    
    Args:
        results: Dict mapping audit title to response text
        output_dir: Directory to save output files
        
    Returns:
        Path to the saved file
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"{today}-leverage-os-run.md"
    filepath = os.path.join(output_dir, filename)

    # If file already exists, add a counter
    counter = 1
    while os.path.exists(filepath):
        filename = f"{today}-leverage-os-run-{counter}.md"
        filepath = os.path.join(output_dir, filename)
        counter += 1

    lines = [
        "---",
        f"date: {today}",
        "tool: leverage-os",
        "source: aws-bedrock",
        "tags: [naval-ravikant, leverage, self-audit]",
        "---",
        "",
        f"# Leverage OS — Full Audit Run ({timestamp})",
        "",
    ]

    for title, content in results.items():
        lines.append(f"## {title}")
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")

    output_text = "\n".join(lines)

    with open(filepath, "w") as f:
        f.write(output_text)

    return filepath
