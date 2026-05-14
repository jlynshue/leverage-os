# Product Requirements Document — Leverage OS

| Field | Value |
|---|---|
| Product | Leverage OS |
| Author | [FILL: author name] |
| Status | Draft |
| Created | 2026-05-11 |
| Last updated | 2026-05-11 |
| Version | 0.1 |

---

## 1. Objectives

### Problem statement

Knowledge workers and solo operators lack a systematic, repeatable process to discover leveraged opportunities from their own data (skills, income, time allocation, career history) and recognize patterns across those discoveries over time. Existing tools are either one-shot (a single brainstorm) or generic (not grounded in the user's actual situation).

### Product vision

A local-first CLI platform that runs structured self-audits against an LLM-agnostic analytical engine, persists results as structured records, detects cross-run patterns automatically, and surfaces actionable opportunity cards with lifecycle management.

### Goals

1. Enable users to discover specific-knowledge niches and leveraged opportunities grounded in their personal data.
2. Recognize patterns (recurring themes, contradictions, drift) across multiple audit runs over time.
3. Provide a decision framework for triaging opportunities (act / defer / discard).
4. Remain provider-agnostic — work with Bedrock, OpenAI, local models, or no AI at all.
5. Stay local-first — no data leaves the machine without explicit per-run opt-in.

### Non-goals

- Multi-user / team collaboration
- Web UI or mobile app
- Cloud sync or SaaS hosting
- Real-time market data integration
- Automated execution of opportunities (this is a discovery tool, not an implementation tool)

---

## 2. Stakeholders

| Role | Name | Responsibility |
|---|---|---|
| Product Owner | [FILL: name] | Scope decisions, charter review, kill criteria |
| Primary User | [FILL: name] | Runs audits, triages opportunities, validates patterns |
| Technical Lead | [FILL: name] | Architecture, provider integrations, eval harness |
| Reviewer | [FILL: name] | Adversarial QA — checks for sloppy reasoning, drift, missing risks |

---

## 3. Scope

### In-scope (v1.0, M0–M4)

- Four Naval Ravikant-style audit frameworks (knowledge, leverage, productize, time-leak)
- LLM provider abstraction (Bedrock, Manual, OpenAI stub)
- Structured run record persistence (`outputs/runs/<id>.json`)
- Cross-run pattern recognition mode (`--audit patterns`)
- Opportunity card lifecycle management (`opp list|update|close`)
- Structural eval harness with fixture personas
- Local-first storage, no network requirement beyond LLM API calls
- Decision log integration

### Out-of-scope (v1.0)

- Web interface or API server
- Multi-tenant / multi-user features
- Integration with external data sources (calendar, finance, CRM)
- Automated outreach or execution
- Mobile application
- Cloud persistence or sync

---

## 4. User / Buyer Personas

### Persona 1: Solo Operator

| Attribute | Detail |
|---|---|
| Role | Solo consultant, indie hacker, or fractional executive |
| Goal | Find the highest-leverage opportunity to pursue next quarter |
| Pain | Stuck in time-for-money work; can't see the pattern across their own decisions |
| Technical comfort | Can run a CLI; has AWS credentials or an OpenAI key |
| Frequency | Runs audit weekly or bi-weekly; reviews patterns monthly |

### Persona 2: [FILL: second persona]

| Attribute | Detail |
|---|---|
| Role | [FILL] |
| Goal | [FILL] |
| Pain | [FILL] |
| Technical comfort | [FILL] |
| Frequency | [FILL] |

---

## 5. Requirements

### 5.1 Functional requirements

| ID | Requirement | Priority | Milestone |
|---|---|---|---|
| FR-01 | CLI runs 4 audit frameworks with user intake answers | Must | M0 (done) |
| FR-02 | Provider seam supports Bedrock, Manual; extensible to others | Must | M0 (done) |
| FR-03 | Each run persists a structured JSON record with run_id, timestamp, provider, model, answers hash, output path | Must | M1 (done) |
| FR-04 | `--audit patterns` mode reads run records and emits pattern cards citing ≥2 source runs | Must | M2 |
| FR-05 | Pattern detection surfaces: recurring themes (≥3 runs), contradictions, drift | Must | M2 |
| FR-06 | `leverage-os opp list\|update\|close` manages opportunity card lifecycle | Should | M3 |
| FR-07 | Each status transition on an opportunity writes a decision-log entry | Should | M3 |
| FR-08 | Second LLM provider (OpenAI or local) validates the abstraction | Should | M4 |
| FR-09 | Eval harness checks structural conformance of model outputs against prompt contracts | Must | Done |
| FR-10 | Fixture personas enable repeatable eval without interactive intake | Must | Done |
| FR-11 | `--no-ai` flag generates filled prompts without API calls | Must | M0 (done) |
| FR-12 | Unknown provider names fall back gracefully to manual | Must | M0 (done) |

### 5.2 Non-functional requirements

| ID | Requirement | Priority |
|---|---|---|
| NFR-01 | All user data stays local; no cloud sync without explicit per-run opt-in | Must |
| NFR-02 | PII masking on any data that leaves the machine (account numbers, SSN, amounts) | Must |
| NFR-03 | Single-run latency < 60s for a single audit on Bedrock Sonnet | Should |
| NFR-04 | Eval harness runs all 3 fixtures × 4 audits in < 5 minutes | Should |
| NFR-05 | Run records are human-readable JSON; no binary formats | Must |
| NFR-06 | CLI works offline with `manual` provider (no network required) | Must |
| NFR-07 | Python 3.10+ compatibility | Must |
| NFR-08 | No paid dependencies for core functionality (boto3 is free; OpenAI key optional) | Should |

---

## 6. Assumptions

1. The user has AWS credentials configured for Bedrock access (or uses `manual` provider).
2. The user runs audits at least 3 times before expecting meaningful pattern detection.
3. Audit prompts produce structurally consistent output ≥80% of the time (target after prompt tightening).
4. A single operator fills all roles (owner, analyst, reviewer) in v1.
5. The user's answers are honest and internally consistent across runs.
6. [FILL: additional assumptions as discovered]

---

## 7. Constraints

| Constraint | Impact |
|---|---|
| Local-first architecture | No server component; all state in `outputs/` directory |
| LLM output non-determinism | Pattern detection must tolerate variance; eval uses overlap thresholds not exact match |
| macOS / Linux only | No Windows testing or support planned for v1 |
| Python ecosystem | All tooling in Python; no polyglot build |
| Bedrock model lifecycle | Models go EOL (already hit once: claude-3-5-sonnet → sonnet-4-6); run records pin model ID for traceability |
| [FILL: budget constraint] | [FILL: monthly API spend cap] |

---

## 8. Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Provider lock-in | Medium | High | LLMProvider abstraction + M4 validation | [FILL] |
| Prompt drift across model versions | High | Medium | Pin model in run log; bump `prompt_framework_version` on edit | [FILL] |
| Cost runaway on repeated eval runs | Low | Medium | `manual` provider fallback; spend cap [FILL] | [FILL] |
| Data sprawl in `outputs/` | High | Low | Schema enforcement; quarterly archive | [FILL] |
| Privacy regression on multi-provider (M4) | Medium | High | Per-provider redaction policy required before merge | [FILL] |
| Eval harness passes but output is low quality | Medium | Medium | Add LLM-as-judge scoring in M2+ (not structural only) | [FILL] |
| User doesn't run enough audits for pattern detection | High | Medium | Minimum 5-run gate before `--audit patterns` activates | [FILL] |

---

## 9. Success Metrics

| Metric | Definition | Target | Measurement |
|---|---|---|---|
| Eval pass rate | Structural conformance checks passing | ≥80% | `python -m leverage_os.evals --provider bedrock` |
| Opportunities surfaced / quarter | Distinct opportunity cards created | [FILL] | Count files in `outputs/opportunities/` |
| Opportunity conversion rate | (acted-on) / (surfaced) | [FILL] | Decision log status transitions |
| Cross-run patterns / month | Pattern cards emitted by `--audit patterns` | [FILL] | Count files in `outputs/patterns/` |
| Time-to-insight | Intake start → first ranked recommendation | [FILL] | Run record timestamp delta |
| Determinism overlap | Jaccard similarity between paired runs (same fixture) | ≥0.35 | Eval harness `--determinism` mode |
| Decision reversal rate | Decisions later flipped in decision log | [FILL] | Decision log analysis |

---

## 10. Milestones

| ID | Milestone | Deliverables | Status | Target date |
|---|---|---|---|---|
| M0 | Scaffolding + provider seam | `docs/SCAFFOLDING.md`, `LLMProvider` protocol, `BedrockProvider`, `ManualProvider` | Done | 2026-05-11 |
| M1 | Structured run records | `outputs/runs/<id>.json` on every CLI run | Done | 2026-05-11 |
| — | Eval harness | `leverage_os/evals.py`, 3 fixture personas, structural conformance checks | Done | 2026-05-11 |
| — | Prompt tightening | Enforce exact output format; eval 28% → 80%+ | In progress | [FILL] |
| M2 | Pattern recognition mode | `--audit patterns`, pattern card emission, ≥2 source run citations | Not started | [FILL] |
| M3 | Opportunity lifecycle | `opp list\|update\|close`, decision-log integration | Not started | [FILL] |
| M4 | Second provider | OpenAI or local impl; redaction policy; cross-provider eval | Not started | [FILL] |

---

## 11. Dependencies

| Dependency | Type | Status | Impact if missing |
|---|---|---|---|
| AWS Bedrock access (us-east-1) | External service | Active | Default provider unavailable; falls back to manual |
| `us.anthropic.claude-sonnet-4-6` model | External service | Active | Must update `BEDROCK_MODEL_ID` if retired |
| Python 3.10+ | Runtime | Available | CLI won't run |
| `boto3`, `questionary`, `rich` | Libraries | Installed | Core functionality broken |
| ≥5 run records in `outputs/runs/` | Data prerequisite (M2) | 1 exists | Pattern detection has insufficient input |
| Prompt tightening (eval ≥80%) | Code prerequisite (M2) | In progress | Pattern cards will have unreliable structure |

---

## 12. Acceptance Criteria

### M0 (Done)

- [x] `docs/SCAFFOLDING.md` exists with all 13 sections
- [x] `LLMProvider` protocol defined with `invoke(prompt) -> str | None`
- [x] `BedrockProvider` produces real output on live Bedrock
- [x] `ManualProvider` returns `None`, triggering filled-prompt fallback
- [x] Unknown provider names log warning and fall back to manual
- [x] `invoke_model()` back-compat wrapper preserves existing `cli.py` call site

### M1 (Done)

- [x] Every CLI run writes `outputs/runs/<run_id>.json`
- [x] Run record contains: run_id, timestamp_utc, audits_run, provider, model, prompt_framework_version, answers_hash, output_path
- [x] `answers_hash` is sha256 (not raw PII)

### Eval harness (Done)

- [x] `python -m leverage_os.evals` runs with no errors in manual mode
- [x] `python -m leverage_os.evals --provider bedrock` produces pass/fail per audit per fixture
- [x] 3 fixture personas (founder, consultant, creator) cover diverse intake profiles

### Prompt tightening (In progress)

- [ ] Eval pass rate ≥ 80% across all 3 fixtures × 4 audits
- [ ] No audit drops below 60% individually

### M2

- [ ] `leverage-os --audit patterns` reads all `outputs/runs/*.json`
- [ ] Emits pattern cards to `outputs/patterns/<id>.md`
- [ ] Each card cites ≥2 source run_ids
- [ ] Detects at least one of: recurring theme, contradiction, or drift
- [ ] Refuses to run with < 5 run records (user-facing message)

### M3

- [ ] `leverage-os opp list` shows all opportunity cards with status
- [ ] `leverage-os opp update <id> --status act` transitions card and writes decision log
- [ ] `leverage-os opp close <id>` marks card as discarded with required rationale
- [ ] Decision log entries at `docs/decisions/<date>-<slug>.md`

### M4

- [ ] Second provider (OpenAI or local) passes eval harness at ≥70%
- [ ] Per-provider redaction policy documented and enforced
- [ ] Cross-provider determinism overlap measured and baselined

---

## 13. Appendices

### A. Technical architecture

```
questions.py → prompts.py → runner.py (LLMProvider) → output.py
                                ↓                        ↓
                         BedrockProvider          save_run_record()
                         ManualProvider           outputs/runs/<id>.json
                         (OpenAI — M4)            outputs/<date>.md
```

### B. Key file paths

| File | Purpose |
|---|---|
| `leverage_os/cli.py` | CLI entry point |
| `leverage_os/runner.py` | Provider seam + `invoke_model` wrapper |
| `leverage_os/prompts.py` | 4 audit prompt builders |
| `leverage_os/questions.py` | Interactive intake |
| `leverage_os/output.py` | Markdown + JSON persistence |
| `leverage_os/evals.py` | Structural eval harness |
| `docs/SCAFFOLDING.md` | Operating manual (governance, templates, processes) |
| `docs/eval-harness-spec.md` | Conformance spec per audit |
| `tests/fixtures/answers_*.json` | Fixture personas |

### C. Related documents

- Scaffolding doc: `docs/SCAFFOLDING.md`
- Eval harness spec: `docs/eval-harness-spec.md`
- Opportunity discovery analysis: `memory/projects/opportunity-discovery.md`
- Pilot fix runbook: `.context/pilot-fix-instructions.md`
- B1 buyer list: `.context/dispatch-results/b1-buyer-list.md`
- B2 competitive scan: `.context/dispatch-results/b2-competitive-scan.md`

---

## 14. Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | What's the monthly API spend cap? | [FILL] | Open |
| 2 | Should M2 pattern detection use LLM or be purely algorithmic? | [FILL] | Open |
| 3 | Is there a second persona beyond solo operator? | [FILL] | Open |
| 4 | What's the minimum viable cadence for pattern detection to be useful? | [FILL] | Open |
| 5 | Should opportunity cards integrate with external tools (Jira, Linear, SP)? | [FILL] | Open |
| 6 | What model should M4 target — OpenAI GPT-4o or local Ollama? | [FILL] | Open |
| 7 | When does the product cross from personal tool to something shippable to others? | [FILL] | Open |
