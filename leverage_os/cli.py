"""Main CLI entry point for Leverage OS."""

import argparse
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .output import save_results, save_run_record, _generate_run_id
from .prompts import ALL_AUDITS, AUDIT_MAP
from .questions import collect_answers
from .runner import invoke_model, DEFAULT_MODEL_ID, DEFAULT_PROVIDER

console = Console()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="leverage-os",
        description="Naval Ravikant-style self-audit CLI — specific knowledge, leverage, productization, and time analysis",
    )
    parser.add_argument(
        "--audit",
        choices=["knowledge", "leverage", "productize", "time-leak", "all"],
        default="all",
        help="Which audit to run (default: all)",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Skip LLM calls — just generate the filled prompts",
    )
    parser.add_argument(
        "--output-dir",
        default="./outputs",
        help="Directory to save results (default: ./outputs)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override Bedrock model ID",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="Override AWS region",
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Normalize audit choice
    audit_key = args.audit.replace("-", "_") if args.audit != "all" else None
    
    # Determine which audits to run
    if audit_key:
        audits_to_run = [audit_key]
    else:
        audits_to_run = ALL_AUDITS

    # Determine filter for questions
    question_filter = audit_key if audit_key else None

    # Collect answers
    try:
        answers = collect_answers(audit_filter=question_filter)
    except (KeyboardInterrupt, EOFError):
        console.print("\n[red]Interrupted. Exiting.[/red]")
        sys.exit(1)

    # Run audits
    results = {}

    console.print()
    console.print(
        Panel(
            "[bold green]Running analyses...[/bold green]",
            border_style="green",
        )
    )
    console.print()

    for audit_key in audits_to_run:
        title, builder = AUDIT_MAP[audit_key]
        prompt = builder(answers)

        if args.no_ai:
            # Just show the filled prompt
            console.print(Panel(f"[bold]{title}[/bold]\n\n[dim]Filled prompt (no AI):[/dim]", border_style="blue"))
            console.print(prompt)
            console.print()
            results[title] = f"**[Prompt Only — No AI Run]**\n\n```\n{prompt}\n```"
        else:
            # Send to Bedrock
            with Progress(
                SpinnerColumn(),
                TextColumn(f"[cyan]Analyzing: {title}...[/cyan]"),
                console=console,
            ) as progress:
                progress.add_task("", total=None)
                response = invoke_model(prompt, model_id=args.model, region=args.region)

            if response:
                console.print(Panel(f"[bold]{title}[/bold]", border_style="green"))
                console.print(Markdown(response))
                console.print()
                results[title] = response
            else:
                # Fallback: show the prompt
                console.print(Panel(f"[bold]{title}[/bold] [red](AI unavailable)[/red]", border_style="yellow"))
                console.print(prompt)
                console.print()
                results[title] = f"**[AI Unavailable — Filled Prompt]**\n\n{prompt}"

    # Save results
    if results:
        filepath = save_results(results, output_dir=args.output_dir)

        run_id = _generate_run_id()
        provider_name = args.model.split(".")[0] if args.model else DEFAULT_PROVIDER
        model_id = args.model or DEFAULT_MODEL_ID
        run_record_path = save_run_record(
            run_id=run_id,
            audits_run=audits_to_run,
            provider_name=provider_name,
            model=model_id,
            answers=answers,
            output_path=filepath,
            output_dir=args.output_dir,
        )

        console.print()
        console.print(
            Panel(
                f"[bold green]Results saved to:[/bold green] {filepath}\n"
                f"[bold green]Run record:[/bold green] {run_record_path}",
                border_style="green",
            )
        )

    console.print("\n[dim]Done. Run again anytime with: leverage-os[/dim]\n")


if __name__ == "__main__":
    main()
