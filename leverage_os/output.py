"""Output module — saves results as markdown files."""

import os
from datetime import datetime
from pathlib import Path

from rich.console import Console

console = Console()


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
