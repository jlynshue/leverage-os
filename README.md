# Leverage OS

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900.svg)](https://aws.amazon.com/bedrock/)

**Strategic self-audit CLI powered by AI. Four Naval Ravikant frameworks applied to your career in one session.**

## Problem

Most professionals never audit their leverage, knowledge, and income-generation patterns. You lack a repeatable, rigorous way to:
- Discover your rare, defensible knowledge
- Identify where you're trading time for money (instead of building equity)
- Design products that scale your expertise
- Track which income streams actually leverage you

Leverage OS fills this gap with AI-powered frameworks that synthesize Naval's thinking into actionable self-analysis.

## How It Works

Answer a consolidated intake questionnaire once. The CLI runs **four asymmetric audit frameworks** via AWS Bedrock (Claude):

| Framework | Output |
|-----------|--------|
| **Specific Knowledge Excavator** | Your rare, defensible knowledge niche + differentiation thesis |
| **Leverage Stack Auditor** | Income streams analyzed for scale, equity, and time-for-money leaks |
| **Productize Yourself Blueprint** | Product/service design that leverages your knowledge without you |
| **Time-for-Money Leak Detector** | Conversion roadmap: rented hours → equity-based income |

All results saved as markdown for versioning and future reference.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CLI Input → Consolidated Questionnaire                     │
│  (career, obsessions, income sources, skills)               │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│  Prompt Framework Layer                                     │
│  ├─ SK Excavator (leverage pattern mining)                  │
│  ├─ Leverage Auditor (income stream analysis)               │
│  ├─ Productize Blueprint (design framework)                 │
│  └─ Time-Leak Detector (equity roadmap)                     │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│  AWS Bedrock API (Claude Model)                             │
│  Parallel inference across 4 frameworks                     │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│  Markdown Output                                            │
│  └─ ./outputs/{date}-leverage-os-{audit-type}.md            │
└─────────────────────────────────────────────────────────────┘
```

## Why Leverage OS?

Generic ChatGPT coaching prompts ask "what are your goals?" and return vague encouragement. Leverage OS applies four rigorous, interlocking frameworks derived from Naval Ravikant's wealth philosophy — each with scoring rubrics, concrete deliverables, and testable claims. The output is a structured audit you can version-control, diff annually, and act on this week — not motivational noise you forget by tomorrow.

## Quick Start

```bash
# Install
pip install -e .

# Configure AWS credentials
aws configure

# Run full audit (all four frameworks)
leverage-os

# Or run individual audits
leverage-os --audit knowledge      # Specific Knowledge Excavator only
leverage-os --audit leverage       # Leverage Stack Auditor only
leverage-os --audit productize     # Productize Yourself Blueprint only
leverage-os --audit time-leak      # Time-for-Money Leak Detector only
```

Results appear in your terminal and are automatically saved to `./outputs/` with ISO timestamps.

## Example Output

Below is a sample Leverage Stack Auditor result for a solo SaaS founder who also does consulting. This is the markdown that gets saved to `./outputs/`.

<details>
<summary><strong>Sample: Leverage Stack Auditor — Solo SaaS Founder</strong></summary>

```markdown
---
date: 2026-06-10
tool: leverage-os
source: aws-bedrock
tags: [naval-ravikant, leverage, self-audit]
---

# Leverage OS — Full Audit Run (2026-06-10 09:42)

## 2. The Leverage Stack Auditor

**Leverage Audit:**

| Activity | Leverage Type | Hours/Week | Score | Revenue % |
|----------|--------------|-----------|-------|-----------|
| Enterprise consulting (data strategy) | Labor | 25 | 1 | 55% |
| SaaS product (analytics dashboard) | Code | 12 | 4 | 30% |
| Technical writing (paid newsletter) | Media | 4 | 3 | 10% |
| Angel investing (2 startups) | Capital | 1 | 5 | 5% |

**Your Leverage Index:** 2.05/5

Calculation: (1 x 55 + 4 x 30 + 3 x 10 + 5 x 5) / 100 = 2.05

**Biggest Leverage Leak:** Enterprise consulting — 25 hours/week generating only 55% of revenue at a leverage score of 1. Every hour here is rented and non-compounding. You are trading your highest-value skill (data architecture) for the lowest-leverage format (live delivery). Opportunity cost: ~15 hours/week that could move your SaaS from $4.5K to $15K MRR.

**3 Upgrade Moves:**

1. **Convert "data strategy workshop" into a self-paced assessment tool** — Package your recurring client diagnostic (the first 3 sessions of every engagement) as an automated scoring workflow inside your SaaS. Score: 1 → 4. Timeline: 21 days.

2. **Turn your top 3 consulting frameworks into a gated case-study series** — Publish "How [anonymized client] reduced data pipeline costs 40% using the 3-Layer Audit" as a 5-part email sequence driving SaaS trials. Score: 1 → 3. Timeline: 14 days.

3. **Raise consulting rate 40% and cap at 15 hrs/week** — Price out low-value clients. Reinvest the freed 10 hours into SaaS feature development (the onboarding funnel you've been deferring). Score: stays 1 but hours drop, effective index rises to 2.6. Timeline: 7 days (send rate increase email Friday).

**30 Day First Move:** This week — extract the "Data Maturity Scorecard" you run in every first consulting session. Build it as a 12-question Typeform connected to a scoring spreadsheet. Gate the detailed results behind a SaaS trial signup. Ship by Friday. Named deliverable: live URL for the Data Maturity Scorecard lead magnet.

---
```

</details>

When displayed in your terminal via Rich, each framework result renders inside a bordered panel with the title highlighted in green, and the markdown tables and headers are fully formatted.

## Tech Stack

| Component | Technology |
|-----------|------------|
| CLI Framework | Python 3.10+ · argparse |
| LLM Backend | AWS Bedrock (Claude) |
| Interactive Input | questionary |
| Output Formatting | rich · markdown |
| Package Management | setuptools |

## Development

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run linting (if configured)
ruff check .

# Format code
ruff format .
```

## Environment

Create a `.env` file (see `.env.example`):

```bash
# Optional: specify AWS profile
AWS_PROFILE=your-profile

# Optional: specify AWS region (defaults to us-east-1)
AWS_REGION=us-west-2
```

## Output Format

Each audit generates a timestamped markdown file:

```
outputs/
├── 2026-06-10-leverage-os-full-run.md      # All four audits
├── 2026-06-10-leverage-os-knowledge.md     # Specific Knowledge Excavator
├── 2026-06-10-leverage-os-leverage.md      # Leverage Stack Auditor
├── 2026-06-10-leverage-os-productize.md    # Productize Yourself Blueprint
└── 2026-06-10-leverage-os-time-leak.md     # Time-for-Money Leak Detector
```

Each file includes:
- Framework name and purpose
- Your input summary
- AI-generated analysis
- Actionable next steps
- Timestamp for version control

## Design Philosophy

**Principle 1: One Session, Four Perspectives**  
Minimize friction. Collect input once; apply all four frameworks in parallel.

**Principle 2: Rigorous Frameworks**  
Don't use generic prompts. Each audit implements a specific thinking model—derived from Naval's essays, decision theory, and business strategy.

**Principle 3: Persistent Output**  
Markdown saved to disk enables versioning. Re-run annually; diff the results to track your evolution.

**Principle 4: Strategic Focus**  
The goal is equity and leverage, not optimization. This tool helps you identify which moves actually compound.

## License

MIT

---

**Author:** [Jonathan Lyn-Shue](https://jonathanlynshue.com) — Fractional CIO/CTO | Data & AI Executive

Built to apply Naval Ravikant's leverage framework to modern knowledge work.
