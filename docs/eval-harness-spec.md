# Eval Harness Spec — leverage-os

Structural conformance spec for the four audit prompts in `leverage_os/prompts.py`.
Each section defines what the model MUST produce, a parser sketch for each field,
and a pass/fail checklist usable as an automated eval.

---

## 1. Specific Knowledge Excavator (`build_knowledge_excavator`, line 4)

### Structural contract

| # | Field | Type | Source line |
|---|---|---|---|
| 1 | `**Your Specific Knowledge Niche:**` | Single sentence | 30 |
| 2 | `**Why This is Rare:**` | 2–3 sentences | 32 |
| 3 | `**3 Leveraged Business Models:**` table | 6 cols × 3 rows | 34–35 |
| 4 | `**Recommended Starting Point:**` | Top model + 3 actions | 37 |

### Table columns (exact)

`Model | Leverage Type | Market | Competition | Multiplier | Score`

### Parser sketch

```python
import re

def parse_knowledge(text: str) -> dict:
    niche = re.search(r'\*\*Your Specific Knowledge Niche:\*\*\s*(.+)', text)
    rare = re.search(r'\*\*Why This is Rare:\*\*\s*(.+?)(?=\n\n|\*\*)', text, re.DOTALL)
    table_rows = re.findall(r'^\|(?!\s*[-:])(.+)\|$', text, re.MULTILINE)
    # Skip header row → data rows are table_rows[1:]
    starting = re.search(r'\*\*Recommended Starting Point:\*\*\s*(.+?)$', text, re.MULTILINE | re.DOTALL)
    return {
        "niche": niche.group(1).strip() if niche else None,
        "rare": rare.group(1).strip() if rare else None,
        "model_rows": [r.split("|") for r in table_rows[1:]] if len(table_rows) > 1 else [],
        "starting_point": starting.group(1).strip() if starting else None,
    }
```

### Conformance checklist

- [ ] Contains literal `**Your Specific Knowledge Niche:**`
- [ ] Niche is a single sentence (≤2 periods)
- [ ] Contains literal `**Why This is Rare:**`
- [ ] Contains literal `**3 Leveraged Business Models:**`
- [ ] Table has exactly 6 columns (pipe-delimited)
- [ ] Table has exactly 3 data rows (excluding header + separator)
- [ ] Each row has `Leverage Type` ∈ {code, media, capital} (never labor)
- [ ] Market, Competition, Multiplier are integers 1–5
- [ ] Score = Market + (6 − Competition) + Multiplier
- [ ] Contains literal `**Recommended Starting Point:**`
- [ ] Starting point mentions ≥3 concrete actions

---

## 2. Leverage Stack Auditor (`build_leverage_auditor`, line 40)

### Structural contract

| # | Field | Type | Source line |
|---|---|---|---|
| 1 | `**Leverage Audit:**` table | 5 cols × N rows | 66–67 |
| 2 | `**Your Leverage Index:**` | Decimal X/5 | 69 |
| 3 | `**Biggest Leverage Leak:**` | Activity + reason + hours | 71 |
| 4 | `**3 Upgrade Moves:**` | Numbered list, 3 items | 73–76 |
| 5 | `**30 Day First Move:**` | Single action + deliverable | 78 |

### Table columns (exact)

`Activity | Leverage Type | Hours/Week | Score | Revenue %`

### Parser sketch

```python
def parse_leverage(text: str) -> dict:
    index = re.search(r'\*\*Your Leverage Index:\*\*\s*(\d+\.?\d*)/5', text)
    leak = re.search(r'\*\*Biggest Leverage Leak:\*\*\s*(.+?)(?=\n\n|\*\*)', text, re.DOTALL)
    moves = re.findall(r'^\d+\.\s*(.+)$', text[text.find('**3 Upgrade Moves:**'):], re.MULTILINE)
    first_move = re.search(r'\*\*30 Day First Move:\*\*\s*(.+?)$', text, re.MULTILINE | re.DOTALL)
    table_rows = re.findall(r'^\|(?!\s*[-:])(.+)\|$', text[:text.find('**Your Leverage Index')], re.MULTILINE)
    return {
        "leverage_index": float(index.group(1)) if index else None,
        "leak": leak.group(1).strip() if leak else None,
        "upgrade_moves": moves[:3],
        "first_move": first_move.group(1).strip() if first_move else None,
        "audit_rows": [r.split("|") for r in table_rows[1:]] if len(table_rows) > 1 else [],
    }
```

### Conformance checklist

- [ ] Contains literal `**Leverage Audit:**`
- [ ] Table has exactly 5 columns
- [ ] Table has ≥1 data row (one per income source)
- [ ] Leverage Type ∈ {Labor, Capital, Code, Media}
- [ ] Score is integer 1–5
- [ ] Contains literal `**Your Leverage Index:**` followed by `X/5` (0.0–5.0)
- [ ] Contains literal `**Biggest Leverage Leak:**`
- [ ] Leak names a specific activity (not generic)
- [ ] Contains literal `**3 Upgrade Moves:**`
- [ ] Exactly 3 numbered items under Upgrade Moves
- [ ] Each move has `Score: [before → after]` and `Timeline: [X days]`
- [ ] Contains literal `**30 Day First Move:**`
- [ ] First move names a concrete deliverable

---

## 3. Productize Yourself Blueprint (`build_productize_blueprint`, line 81)

### Structural contract

| # | Field | Type | Source line |
|---|---|---|---|
| 1 | `**Your Core Transformation:**` | I help [WHO]… template | 109–110 |
| 2 | `**3 Product Formats:**` table | 4 cols × 3 rows | 112–113 |
| 3 | `**Winning Product Structure:**` | 4 named fields | 115–120 |
| 4 | `**Launch Positioning:**` | Single sentence | 122 |
| 5 | `**Week 1 Roadmap:**` | 3 tasks | 123 |

### Table columns (exact)

`Format | Leverage | Feasibility | Margin | Score`

### Parser sketch

```python
def parse_productize(text: str) -> dict:
    transform = re.search(r'\*\*Your Core Transformation:\*\*\s*(.+?)(?=\n\n|\*\*)', text, re.DOTALL)
    table_rows = re.findall(r'^\|(?!\s*[-:])(.+)\|$', text, re.MULTILINE)
    name = re.search(r'Name:\s*(.+)', text)
    contents = re.search(r'Contents:\s*(.+)', text)
    delivery = re.search(r'Delivery:\s*(.+)', text)
    price = re.search(r'Price point:\s*(.+)', text)
    positioning = re.search(r'\*\*Launch Positioning:\*\*\s*(.+)', text)
    roadmap = re.findall(r'^\d+\.\s*(.+)$', text[text.find('**Week 1 Roadmap:**'):], re.MULTILINE)
    return {
        "transformation": transform.group(1).strip() if transform else None,
        "format_rows": [r.split("|") for r in table_rows[1:4]] if len(table_rows) > 1 else [],
        "product_name": name.group(1).strip() if name else None,
        "product_contents": contents.group(1).strip() if contents else None,
        "product_delivery": delivery.group(1).strip() if delivery else None,
        "product_price": price.group(1).strip() if price else None,
        "positioning": positioning.group(1).strip() if positioning else None,
        "roadmap_tasks": roadmap[:3],
    }
```

### Conformance checklist

- [ ] Contains literal `**Your Core Transformation:**`
- [ ] Transformation matches pattern `I help [WHO] go from [BEFORE] to [AFTER] using [NAMED METHOD]`
- [ ] Contains literal `**3 Product Formats:**`
- [ ] Table has exactly 5 columns (Format + 3 scores + total)
- [ ] Table has exactly 3 data rows
- [ ] Leverage, Feasibility, Margin are integers 1–5
- [ ] Score = Leverage + Feasibility + Margin
- [ ] Contains literal `**Winning Product Structure:**`
- [ ] Contains all four fields: Name, Contents, Delivery, Price point
- [ ] Name includes a proprietary-sounding mechanism name
- [ ] Delivery does NOT require live presence
- [ ] Contains literal `**Launch Positioning:**` (single sentence)
- [ ] Contains literal `**Week 1 Roadmap:**`
- [ ] Exactly 3 tasks, each ≤4 hours

---

## 4. Time-for-Money Leak Detector (`build_time_leak_detector`, line 125)

### Structural contract

| # | Field | Type | Source line |
|---|---|---|---|
| 1 | `**Time Audit:**` table | 5 cols × N rows | 153–154 |
| 2 | `**Your Time Rent Ratio:**` | X% rented / Y% equity | 156 |
| 3 | `**Top 3 Conversion Opportunities:**` | Numbered, 3 items | 158–161 |
| 4 | `**The Equity Gap:**` | 24-month projection with math | 163 |
| 5 | `**First Escape Move:**` | One action + deliverable | 165 |

### Table columns (exact)

`Activity | Type | Hours/Week | Equity Potential (1-5) | Conversion Difficulty`

### Parser sketch

```python
def parse_time_leak(text: str) -> dict:
    ratio = re.search(r'\*\*Your Time Rent Ratio:\*\*\s*(\d+)%\s*rented\s*/\s*(\d+)%\s*equity', text)
    conversions = re.findall(r'^\d+\.\s*(.+)$', text[text.find('**Top 3 Conversion'):], re.MULTILINE)
    gap = re.search(r'\*\*The Equity Gap:\*\*\s*(.+?)(?=\n\n\*\*|\Z)', text, re.DOTALL)
    escape = re.search(r'\*\*First Escape Move:\*\*\s*(.+?)$', text, re.MULTILINE | re.DOTALL)
    table_rows = re.findall(r'^\|(?!\s*[-:])(.+)\|$', text[:text.find('**Your Time Rent')], re.MULTILINE)
    return {
        "rented_pct": int(ratio.group(1)) if ratio else None,
        "equity_pct": int(ratio.group(2)) if ratio else None,
        "conversions": conversions[:3],
        "equity_gap": gap.group(1).strip() if gap else None,
        "escape_move": escape.group(1).strip() if escape else None,
        "audit_rows": [r.split("|") for r in table_rows[1:]] if len(table_rows) > 1 else [],
    }
```

### Conformance checklist

- [ ] Contains literal `**Time Audit:**`
- [ ] Table has exactly 5 columns
- [ ] Table has ≥1 data row
- [ ] Type ∈ {Time Rented, Equity Building}
- [ ] Equity Potential is integer 1–5
- [ ] Conversion Difficulty ∈ {Low, Medium, Med, High}
- [ ] Contains literal `**Your Time Rent Ratio:**`
- [ ] Ratio percentages sum to 100 (±1 rounding)
- [ ] Contains literal `**Top 3 Conversion Opportunities:**`
- [ ] Exactly 3 numbered items
- [ ] Each has Effort and Leverage fields
- [ ] Contains literal `**The Equity Gap:**`
- [ ] Gap section includes numeric calculation (shows compound math)
- [ ] Contains literal `**First Escape Move:**`
- [ ] Escape move names a concrete deliverable

---

## 5. Determinism Overlap Recipe

Measures how stable the model's output is across two runs with identical fixture answers.

```python
import re
from collections import Counter

STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "to", "of", "in", "for",
             "and", "or", "but", "with", "on", "at", "by", "from", "that", "this",
             "it", "i", "my", "you", "your"}

def tokenize(text: str) -> set[str]:
    words = re.findall(r'[a-z]+', text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}

def overlap_ratio(run_a: str, run_b: str) -> float:
    """Jaccard similarity of keyword sets between two runs."""
    a, b = tokenize(run_a), tokenize(run_b)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def section_overlap(run_a: str, run_b: str, header: str) -> float:
    """Overlap for a specific section only (e.g. the niche sentence)."""
    def extract(text):
        match = re.search(rf'\*\*{re.escape(header)}\*\*\s*(.+?)(?=\n\n\*\*|\Z)', text, re.DOTALL)
        return match.group(1) if match else ""
    return overlap_ratio(extract(run_a), extract(run_b))
```

### Determinism thresholds (suggested baselines)

| Audit | Section | Expected overlap (same fixture) |
|---|---|---|
| knowledge | Niche sentence | ≥ 0.40 |
| knowledge | Full output | ≥ 0.30 |
| leverage | Leverage Index value | exact match |
| leverage | Full output | ≥ 0.35 |
| productize | Core transformation | ≥ 0.35 |
| time_leak | Rent ratio percentages | ±5% |

These are floor targets — actual baseline to be established from 5 paired runs per fixture.

---

## 6. Fixture Personas (for test runs)

Minimum 3 fixtures needed — enough to cover variation. Schema:

```json
{
  "persona": "founder",
  "answers": {
    "obsessions": "agent orchestration, leverage theory, operational AI",
    "career_path": "Enterprise PM → startup CTO → solo AI consultant",
    "undervalued_skills": "translating technical systems into business frameworks, cold outreach",
    "income_sources": "Consulting: 30hrs/wk, 70% | SaaS side project: 5hrs/wk, 20% | Speaking: 2hrs/wk, 10%",
    "monthly_income_target": "$20,000",
    "skills_assets": "AI agent framework, 3 open-source tools, advisory network",
    "expertise_transformation": "Help mid-market ops teams go from manual workflows to AI-augmented operations",
    "platforms_audiences": "LinkedIn (2k followers), GitHub (500 stars across repos)",
    "hours_available": "15",
    "work_activities": "Client consulting: hourly | SaaS: subscription | Speaking: per-event",
    "total_hours_weekly": "40",
    "current_monthly_income": "$18,000",
    "income_split": "85% active / 15% passive"
  }
}
```

Store at `tests/fixtures/answers_founder.json`. Add `answers_consultant.json` and `answers_creator.json` with different profiles.
