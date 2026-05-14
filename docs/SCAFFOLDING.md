# Leverage OS — Scaffolding

> **Goal (do not alter):** discover opportunities and recognize patterns.

This document is the operating manual for `leverage-os` as a durable
opportunity-discovery and pattern-recognition platform. It is intentionally
self-contained — every artifact, template, and process needed to run the project
lives below as a copy-pasteable section. Sections marked `[FILL: …]` are
placeholders for project-specific information you supply later (see Appendix in §13).

**Conflict-resolution rule:** if two instructions in this doc disagree, prioritize
in this order — (1) constraints / do-nots, (2) required outputs, (3) examples /
references.

---

## 1. Project Charter

**Mission.** Turn personal data and structured self-audits into a durable loop that
discovers leveraged opportunities and recognizes patterns across them over time.

**Goal.** Discover opportunities and recognize patterns.

**In-scope (M0–M4):**

- The four existing audits (knowledge, leverage, productize, time-leak)
- A swappable analytical engine (`LLMProvider`)
- Persisting structured run records and opportunity / pattern cards
- Local-first storage in `outputs/`
- Cross-run pattern recognition as a first-class CLI mode

**Out-of-scope (this scaffolding pass):**

- Multi-user / cloud sync
- A web UI
- Anything that exfiltrates personal data outside the local machine without
  explicit, per-run opt-in

**Project brief.** `[FILL: project brief]`

**Target domain / context.** `[FILL: target domain or context]`

**Stakeholders & roles.** `[FILL: stakeholders and roles]` — see §3 for the
default role split if this is a single-operator project.

**Timeline.** `[FILL: timeline]` — see §8 for milestone sequencing.

**Success metrics.** `[FILL: success metrics]`. Starter set, adopt or replace:

| Metric | Definition | Target |
|---|---|---|
| Opportunities surfaced / quarter | Count of distinct opportunity cards created | `[FILL]` |
| Opportunity conversion rate | (acted-on) / (surfaced) | `[FILL]` |
| Cross-run patterns / month | Pattern cards detected by engine vs. manually | `[FILL]` |
| Time-to-insight | Intake start → first ranked recommendation | `[FILL]` |
| Decision reversal rate | Decisions later flipped, from decision log | `[FILL]` |

---

## 2. Governance & Decision Rights

**Decision types tracked.**

| Type | Example | Logged where |
|---|---|---|
| Scope | Adding a new audit framework | Decision log (§5) |
| Data | Persisting a new field, retention change | Decision log + §6 |
| Engine / provider | Switching default LLM provider | Decision log + run log |
| Prompt-framework changes | Editing a prompt in `prompts.py` | Decision log + version bump |
| Releases | Cutting a new version tag | Decision log |

**Cadence.**

- **Weekly self-review (15 min):** triage new opportunity cards, mark dead ones.
- **Monthly pattern retro (45 min):** run `--audit patterns` (M2+), review pattern
  cards, update charter assumptions.
- **Quarterly charter review (60 min):** revisit goal, scope, metrics, kill criteria.

**RACI template.**

| Activity | R (Responsible) | A (Accountable) | C (Consulted) | I (Informed) |
|---|---|---|---|---|
| Run audit | `[FILL]` | `[FILL]` | — | — |
| Triage opportunities | `[FILL]` | `[FILL]` | — | — |
| Approve prompt changes | `[FILL]` | `[FILL]` | `[FILL]` | — |
| Approve provider switch | `[FILL]` | `[FILL]` | — | — |
| Quarterly charter review | `[FILL]` | `[FILL]` | `[FILL]` | `[FILL]` |

**Conflict resolution.** Constraints / do-nots win over required outputs, which win
over examples / references. Document the resolution in the decision log.

---

## 3. Roles & Responsibilities

For a single-operator project, all four roles map to the same person — but keep the
*function* separate so context-switching is explicit.

| Role | Responsibility |
|---|---|
| **Owner** | Owns charter, metrics, kill criteria. Approves scope changes. |
| **Operator** | Runs the CLI, captures intake honestly, files opportunities. |
| **Analyst** | Reviews outputs, scores opportunities, writes pattern cards. |
| **Reviewer** | Adversarial check: looks for missing risks, sloppy reasoning, drift. |

---

## 4. Processes & Workflows

Five named loops. Each loop has explicit inputs, outputs, and the code path
(if any) that implements it today.

### 4.1 Intake loop

- **Input:** operator answers to `leverage_os/questions.py:QUESTIONS`.
- **Output:** an in-memory `answers` dict (M0); a persisted `outputs/runs/<id>.json`
  record (M1).
- **Code:** `leverage_os/questions.py::collect_answers`.
- **Rule:** never edit answers after the run starts — re-run instead.

### 4.2 Analysis loop

- **Input:** `answers` dict + selected audit framework(s).
- **Output:** filled prompt(s) + provider response(s).
- **Code:** `leverage_os/cli.py::main` calls `leverage_os/runner.py::invoke_model`,
  which delegates to the active `LLMProvider` (see §7).
- **Rule:** the *prompt* is the contract; provider swaps must not silently change
  prompt content.

### 4.3 Pattern-recognition loop *(M2+)*

- **Input:** all run records under `outputs/runs/*.json` plus their markdown outputs.
- **Output:** zero or more pattern cards (§5) appended to `outputs/patterns/`.
- **Code (planned):** `leverage-os --audit patterns` mode.
- **Process:**
  1. Load run records since last retro.
  2. Group opportunity cards by `niche` and `leverage_type`.
  3. Surface: recurring themes (≥3 runs), contradictions (same input → divergent
     output), drift (stable input → output trending in one direction).
  4. Emit one pattern card per finding, citing source `run_id`s.
- **Rule:** every pattern card cites at least two source runs. Single-run
  observations are *not* patterns.

### 4.4 Opportunity-triage loop

- **Input:** new opportunity cards (§5) created from a run's output.
- **Output:** each card moves to one of `act` / `defer` / `discard`, with a
  decision-log entry.
- **Process:**
  1. Score (existing rubric: market + (6 − competition) + multiplier).
  2. Apply triage filter: act on top 1–2 per quarter; defer the rest with a
     review date; discard anything failing the "too generic" test.
  3. Log the decision (§5 template).
- **Rule:** never act on more than two opportunities concurrently — concurrency
  destroys the leverage that surfaces them.

### 4.5 Retro loop

- **Cadence:** monthly (pattern retro) and quarterly (charter retro).
- **Input:** decision log + opportunity cards + pattern cards.
- **Output:** updated charter sections (this doc), risk register entries,
  potentially a kill-criteria trigger.
- **Anchor question (monthly):** *what pattern did we see this month that we
  wouldn't have seen last month?*

---

## 5. Artifacts & Templates

Copy-paste these directly. Each is the canonical schema for its artifact.

### 5.1 Run log entry — `outputs/runs/<run_id>.json`

```json
{
  "run_id": "2026-05-10T14-32-08Z-ab12",
  "timestamp_utc": "2026-05-10T14:32:08Z",
  "audits_run": ["knowledge", "leverage"],
  "provider": "bedrock",
  "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "prompt_framework_version": "0.1.0",
  "answers_hash": "sha256:…",
  "output_path": "outputs/2026-05-10-leverage-os-full-run.md",
  "opportunities_extracted": 3,
  "notes": ""
}
```

### 5.2 Opportunity card — `outputs/opportunities/<opp_id>.md`

```markdown
---
opp_id: OPP-2026-05-10-001
source_run_id: 2026-05-10T14-32-08Z-ab12
niche: "[one-sentence specific niche]"
leverage_type: code | media | capital
score:
  market: 4
  competition: 2
  multiplier: 5
  total: 13
status: act | defer | discard
next_action: "[concrete first action, ≤14 days]"
owner: "[FILL]"
review_date: 2026-06-10
---

## Why this is rare
…

## How it generates leverage
…

## First 14 days
1. …
2. …
3. …
```

### 5.3 Pattern card — `outputs/patterns/<pattern_id>.md`

```markdown
---
pattern_id: PAT-2026-Q2-001
observation: "[one-sentence pattern]"
supporting_runs:
  - 2026-04-12T…
  - 2026-04-26T…
  - 2026-05-10T…
confidence: low | medium | high
detector: engine | manual
hypothesis: "[what this pattern implies]"
test: "[concrete next observation that would confirm or kill it]"
---

## Evidence
- Run X said …
- Run Y said …

## Implications for charter
…
```

### 5.4 Decision log entry — `docs/decisions/<yyyy-mm-dd>-<slug>.md`

```markdown
---
date: 2026-05-10
decision: "[one-line decision]"
type: scope | data | engine | prompt | release
reversible: true | false
---

## Context
…

## Alternatives considered
1. …
2. …

## Rationale
…

## Follow-ups
- [ ] …
```

### 5.5 Risk register row

```markdown
| Risk | Likelihood | Impact | Owner | Mitigation | Status |
|---|---|---|---|---|---|
| Provider lock-in | Med | High | [FILL] | LLMProvider abstraction (§7) | Mitigated (M0) |
| Prompt drift across model versions | High | Med | [FILL] | Pin model in run log; bump prompt_framework_version on edit | Active |
| Cost runaway | Low | Med | [FILL] | `manual` provider fallback; daily spend cap [FILL] | Monitored |
| Data sprawl in outputs/ | High | Low | [FILL] | Schema in §6; quarterly archive | Active |
| Privacy regression on multi-provider | Med | High | [FILL] | Per-provider redaction policy (§6) | Pending (blocks M4) |
```

### 5.6 Charter / RACI / cadence templates

See §1 (charter), §2 (RACI + cadence). Reuse those tables verbatim.

---

## 6. Data Requirements

### 6.1 Sources

| Source | Status | Notes |
|---|---|---|
| `outputs/*.md` (audit results) | Exists today | Markdown; unstructured |
| Intake answers | Ephemeral today | **Gap** — persist as `outputs/runs/<id>.json` (M1) |
| Calendar / finances / journal | Future | Domain-dependent: `[FILL: target domain]` |
| Decision log | Future | `docs/decisions/` (M1+) |

### 6.2 Schema (sketch)

The artifacts in §5 are the canonical schemas. Treat them as JSON Schema sources of
truth — when you change a field, bump `prompt_framework_version` in the run log so
older runs remain interpretable.

### 6.3 Retention & privacy

- All outputs stay local under `outputs/`. No cloud sync without explicit per-run
  opt-in.
- PII masking rules inherited from `code-projects/CLAUDE.md` apply to anything
  that ever leaves the machine: account numbers → `XXXX-1234`, amounts → `$XXX.XX`,
  merchants → `[MERCHANT]`, SSN → `000-00-0000`.
- Per-provider redaction policy is required before adding any non-local provider
  (see risk register, §5.5).

### 6.4 Provenance

- Every opportunity card cites exactly one `source_run_id`.
- Every pattern card cites ≥2 `supporting_runs`.
- Every decision log entry references the artifacts it acted on.

No artifact is admissible in a retro without provenance.

---

## 7. Engine Abstraction (LLM-agnostic)

The analytical engine is swappable via the `LLMProvider` protocol in
`leverage_os/runner.py`.

### 7.1 Protocol

```python
class LLMProvider(Protocol):
    name: str
    def invoke(self, prompt: str) -> str | None: ...
```

A provider returns the model response text, or `None` to trigger the CLI's existing
"AI unavailable — filled prompt" fallback (`leverage_os/cli.py:114-119`).

### 7.2 Built-in providers

| Name | Status | Behavior |
|---|---|---|
| `bedrock` | Default | Calls AWS Bedrock with `BEDROCK_MODEL_ID` |
| `manual` | Available | Returns `None` — forces filled-prompt fallback (no API calls) |
| `openai` | Reserved | Stub for M4 — not yet implemented |

### 7.3 Selection precedence

1. Explicit `--provider` CLI flag (planned, not yet wired)
2. `LEVERAGE_OS_PROVIDER` env var (see `.env.example`)
3. Hard-coded default: `bedrock`

Unknown provider names log a warning and fall back to `manual`.

### 7.4 Adding a provider

1. Implement a class with a `name` attribute and `invoke(self, prompt) -> str | None`.
2. Register it in `_PROVIDERS` in `leverage_os/runner.py`.
3. Add a redaction policy (§6.3) before merging if the provider sends data off-box.
4. Bump `prompt_framework_version` only if you change prompts.

---

## 8. Milestones & High-Level Timeline

| ID | Milestone | Outputs | Dates |
|---|---|---|---|
| **M0** | Scaffolding + provider seam | This doc; `LLMProvider` in `runner.py`; `.env.example` updated | `[FILL]` |
| **M1** | Persist structured run records | `outputs/runs/<id>.json` written each run; opportunity-card extractor (manual fine) | `[FILL]` |
| **M2** | `--audit patterns` mode | New CLI mode emitting pattern cards from `outputs/runs/` | `[FILL]` |
| **M3** | Opportunity-card lifecycle | `leverage-os opp list/update/close` commands + decision-log integration | `[FILL]` |
| **M4** | Second provider | `OpenAIProvider` (or local) implemented; redaction policy in place | `[FILL]` |

---

## 9. Risk Management

See risk-register template in §5.5 for ongoing tracking. Starter risks already populated
there. Review monthly during the pattern retro.

---

## 10. Success Criteria & Review

**Quantitative.** See §1 metrics table.

**Qualitative.** Monthly retro must answer: *what pattern did we see this month that
we wouldn't have seen last month?* If the answer is "nothing" three months in a row,
trigger a charter review.

**Kill criteria.** If after 2 quarters zero opportunities have been moved to `act`
status, the charter is re-opened — either the goal, the scope, or the engine is
wrong.

---

## 11. Execution Checklist

- [x] Identify project goal and success criteria.
- [x] Define governance and decision rights.
- [x] List required artifacts and templates.
- [x] Specify data requirements and sources.
- [x] Outline processes and workflows.
- [x] Establish milestones and timelines.
- [x] Include risk management and mitigation.
- [x] Provide placeholders for missing information.
- [x] Deliver copy/paste-ready scaffolding plan.

---

## 12. Conflict Resolution Note

If two instructions in this doc, in code, or in user requests disagree, resolve in
this order:

1. **Constraints / do-nots** (privacy, kill criteria, "do not alter the goal")
2. **Required outputs** (the artifacts in §5)
3. **Examples / references** (everything else)

Record the resolution in the decision log (§5.4).

---

## 13. Appendix — Placeholders Index

Every `[FILL: …]` in this doc, in one place. Fill these once and grep to verify none remain.

| Section | Placeholder | Meaning |
|---|---|---|
| §1 | `[FILL: project brief]` | One-paragraph project brief |
| §1 | `[FILL: target domain or context]` | Domain (e.g. solo founder, indie hacker, exec) |
| §1 | `[FILL: stakeholders and roles]` | Names mapped to §3 roles |
| §1 | `[FILL: timeline]` | Calendar dates for M0–M4 |
| §1 | `[FILL: success metrics]` | Replace or accept the starter table |
| §1 metrics targets | `[FILL]` (×5) | Numeric targets for each metric |
| §2 RACI | `[FILL]` (multiple) | Role assignments per activity |
| §5.2 opportunity card | `owner: "[FILL]"` | Per-card owner field |
| §5.5 risk register | `[FILL]` (owner column) | Risk owners |
| §5.5 risk register | `daily spend cap [FILL]` | Cost cap value |
| §6.1 | `[FILL: target domain]` | Same value as §1 |
| §8 milestones | `[FILL]` (dates) | Calendar dates per milestone |
