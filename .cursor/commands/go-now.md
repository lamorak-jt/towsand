---
description: Implement tasks from the project task list following the project structure and rules
alwaysApply: false
---

# Go Now Command

Implement tasks from `project/task-list.md` to build the Towsand portfolio management system. Work systematically through phases, respecting portfolio management rules and strategy documents. Do NOT theorise — implement.

**Command Format**: `/go-now [optional task identifier or phase number]`

---ORIENTATION---
Towsand is a local Python + SQLite system that tracks the Townsend family portfolio, enforces portfolio management rules, and recommends buy/sell actions to maximise risk-adjusted returns. The project is in **early build phase** — foundational infrastructure and core features are being implemented. We need high development velocity with a clean, extensible foundation.

**Overall Objective**: Maximise risk-adjusted returns for the Townsend family over the timeframes dictated in strategy documents.

**Core Documents** (read these first):
- `project/project-overview.md` — overall objective
- `project/task-list.md` — phased implementation plan (source of truth for tasks)
- `current-finances/portfolio-management-rules.md` — portfolio rules to enforce
- `current-finances/strategy-assumptions.md` — strategy context and assumptions
- `current-finances/institutions.md` — current account structure

**Tech Stack**:
- Python 3.12+ with SQLite3 (stdlib)
- Click for CLI interface
- yfinance (or similar) for market data
- pandas for data manipulation
- Flask/FastAPI for lightweight web UI (read-only dashboard)
- No ORM — direct SQLite usage

**Minimum Guards** (must pass to proceed):
- Python 3.12+; SQLite3 for persistence; Click for CLI; yfinance/pandas for market data.
- Resource safety: context-managed database connections; proper transaction handling.
- Data integrity: cite data sources (dataset name, reference period); respect instrument classifications (capital role, macro drivers, corporate groups).
- Portfolio rules: all compliance checks must align with `current-finances/portfolio-management-rules.md`.
- Functions ≤ ~80 logical lines; cyclomatic complexity ≤10 where practical.

**Repository Conventions**:
- Code files: `src/` directory with subdirectories (`db/`, `market_data/`, `compliance/`, `recommendations/`, `cli/`, `ui/`, `tests/`)
- Database: SQLite file at `data/towsand.db` (or configurable path)
- Configuration: `pyproject.toml` for dependencies; `requirements.txt` for lock file
- Documentation: markdown files in `project/`, `current-finances/`
- Naming: snake_case for code files and schemas; Capitalized-Kebab-Case for documentation

**Citation & Edits** (strict):
- Existing code: cite using CODE REFERENCES with line numbers:
  ```12:24:src/path/to/file.py
  # code excerpt
  ```
- New or replacement code: fenced blocks with a language tag (no line numbers inside):
  ```python
  def example():
      return "ok"
  ```
- Never mix formats; keep edits minimal and well-scoped; preserve indentation/formatting.

If anything is unclear or conflicts with these rules: STOP and ask precise questions before editing. Do not charge ahead.
---END ORIENTATION---

## Inputs
- Optional: Task identifier (e.g. "Phase 1.2", "4.1", or specific task description)
- If user does NOT specify: continue with the next uncompleted task in the current phase
- If unclear which task to work on: STOP and ask the user to specify

## Requirements
- Follow `project/task-list.md` as the source of truth for tasks
- Read and enforce portfolio rules from `current-finances/portfolio-management-rules.md`
- Align with strategy assumptions from `current-finances/strategy-assumptions.md`
- Respect the dependency order: Phase 1 → Phase 2 → Phase 3 → Phase 4/5 → Phase 6 → Phase 7/8

## Execution

### 1. Resolve task target
- If user provided a task identifier: locate it in `project/task-list.md`
- If user said "continue" or "next": find the first uncompleted task in the current phase
- If neither is clear: STOP and ask: "Which task should I implement? Please specify a phase/task identifier from project/task-list.md"

### 2. Load context
- Read: `project/task-list.md` to understand the task and its dependencies
- Read: `project/project-overview.md` for overall objective
- Read: `current-finances/portfolio-management-rules.md` for rule definitions (if compliance-related)
- Read: `current-finances/strategy-assumptions.md` for strategy context (if needed)
- Read: `current-finances/institutions.md` for account structure (if data-related)
- Check existing code structure in `src/` to understand current implementation state

### 3. Implement task
- **Understand**: Extract requirements, acceptance criteria, and constraints from the task description
- **Plan**: Produce Edit Plan (grouped by file) with CODE REFERENCES to current context
- **Implement**: Apply edits in small, reviewable steps. Respect guardrails (typing, data integrity, portfolio rules)
- **Validate**: Provide runnable test commands and expected outputs (CLI commands, database queries, etc.)
- **Update task list**: Mark completed tasks in `project/task-list.md` with `[x]`; add brief implementation notes if helpful

### 4. Guardrails (non-negotiable)
- Database integrity: proper transaction handling; foreign key constraints; data validation
- Portfolio rules: all compliance checks must match `current-finances/portfolio-management-rules.md` exactly
- Data integrity: cite data sources (dataset name, reference period); respect instrument classifications
- Performance: efficient SQL queries; avoid N+1 patterns; use indexes where appropriate
- Functions ≤ ~80 logical lines; cyclomatic complexity ≤10
- Do NOT modify existing data or destroy databases without explicit approval

### 5. Output format
- Edit Plan (grouped by file, with CODE REFERENCES)
- Edits (PR-ready, minimal, well-scoped)
- Tests & Evidence (CLI commands, expected outputs, database queries)
- Validation Checklist (all items ticked)
- Implementation Notes (summary, any deviations from plan, follow-up tasks)

### 6. Safety
- Do not modify existing portfolio data without explicit approval
- Do not restart services or modify environment configuration
- Preserve existing database schema unless migration is explicitly required
- If anything conflicts or is unclear: STOP and ask precise questions before editing

## Notes
- Task list: `project/task-list.md` is the authoritative source for what needs to be built
- Phase dependencies: respect the dependency order shown in the task list
- Database: SQLite file at `data/towsand.db` (create directory if needed)
- CLI: root command is `towsand` (Click-based command group)
- Take small, high-accuracy steps — don't try to complete entire phases in one run
- When in doubt, refer to portfolio management rules and strategy assumptions documents