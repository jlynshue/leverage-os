# Leverage OS

A CLI tool for running Naval Ravikant-style self-audits using AI. Answer questions once, get four comprehensive analyses:

1. **The Specific Knowledge Excavator** — Find your rare knowledge niche
2. **The Leverage Stack Auditor** — Audit income streams for leverage leaks
3. **The Productize Yourself Blueprint** — Design products that sell without you
4. **The Time-for-Money Leak Detector** — Convert rented hours into equity

## Setup

```bash
cd projects/active/leverage-os
pip install -e .
```

## Configuration

Uses AWS Bedrock for LLM calls. Ensure your AWS credentials are configured:

```bash
aws configure
# or export AWS_PROFILE=your-profile
```

## Usage

```bash
leverage-os
```

The CLI will:
1. Ask you a consolidated set of questions (obsessions, career path, income sources, etc.)
2. Generate four filled prompt frameworks
3. Send each to Claude via AWS Bedrock
4. Display results in the terminal
5. Save results as markdown in `./outputs/`

## Running Individual Audits

```bash
leverage-os --audit knowledge    # Only run Specific Knowledge Excavator
leverage-os --audit leverage     # Only run Leverage Stack Auditor
leverage-os --audit productize   # Only run Productize Yourself Blueprint
leverage-os --audit time-leak    # Only run Time-for-Money Leak Detector
```

## Output

Results are saved to `./outputs/` with timestamps:
```
outputs/2026-05-10-leverage-os-full-run.md
```
