---
description: Git commit, lint, fix, and push workflow
alwaysApply: false
---

# Do Git Command

When the user invokes `/do-git`, execute a complete git workflow: commit changes, run linters, fix issues, and push.

**Command Format**: `/do-git [optional commit message]`

---ORIENTATION---
Robbot is a labour-market intelligence app built for Jobs and Skills Australia (JSA) stakeholders. It is at the **early build phase** — foundational infrastructure and first features are being designed and implemented. We need high development velocity with a clean, extensible foundation. Therefore, follow, without deviation:

- project/rules/code-rules.md

Minimum Guards (must pass to proceed)
- Python 3.12+; FastAPI for the backend API; Vite + React + TypeScript for the frontend.
- Async/resource safety: no blocking I/O in async paths; context-managed clients/sessions.
- API typing: Pydantic v2 request/response models; explicit error handling; never return ORM instances.
- Frontend a11y (if applicable): semantic HTML; keyboard flows; visible focus; proper ARIA.
- Data integrity: cite data sources (dataset name, reference period); respect classification systems (ANZSCO, ANZSIC, SA2/SA4).

Repository Conventions
- Roadmap files live under `project/roadmap/**`; case is significant (Linux). Use relative paths; Capitalized-Kebab-Case for roadmap design/docs; snake_case for code files and schemas.
- Keep functions ≤ ~80 logical lines; cyclomatic complexity ≤10 where practical (see `project/rules/code-rules.md`).

Citation & Edits (strict)
- Existing code: cite using CODE REFERENCES with line numbers:
  ```12:24:backend/path/to/file.py
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

## Workflow Steps

### 1. Write commit message and commit
- **CRITICAL**: Only process unstaged or uncommitted changes. Check `git status` to identify:
  - Modified files not yet staged (`git diff`)
  - Staged changes (`git diff --cached`)
  - Untracked files
- If user provided a commit message, use it
- If no message provided, analyze ONLY the unstaged/staged changes and generate a descriptive commit message
- Commit ONLY staged changes: `git commit -m "<message>"`
- If nothing is staged, check `git status` and ask user if they want to stage all modified files
- **Never commit already-committed changes** - only work with current working directory state

### 2. Run linters defined in pyproject.toml
- **CRITICAL**: Only lint files that have unstaged or uncommitted changes
- First, identify changed files: `git diff --name-only` and `git diff --cached --name-only`
- Filter to only Python files in `backend/` or `tests/` directories
- Ensure `backend/venv` is activated (check with `which python` should show `backend/venv/bin/python`)
- Run Ruff linter ONLY on changed files: `python -m ruff check <changed-files>`
- If no changed files, skip linting and inform user
- Capture all linter output (errors, warnings, suggestions) for ONLY the changed files
- Count total lines of feedback

### 3. Address feedback according to project/rules/code-rules.md
- **CRITICAL**: Only fix linter issues in files that have unstaged or uncommitted changes
- Read `project/rules/code-rules.md` to understand coding standards
- For each linter issue in changed files only:
  - Apply fixes that align with `project/rules/code-rules.md`
  - Use `ruff check --fix <changed-files>` for auto-fixable issues when appropriate
  - Manually fix issues that require code changes per `project/rules/code-rules.md`
  - Respect per-file ignores and project-specific patterns
- Re-run linter on changed files after fixes to verify resolution
- **Ignore linter errors in files that are not part of the current changes**

### 4. Handle large feedback (>500 lines)
- If linter feedback exceeds 500 lines:
  - STOP fixing automatically
  - Summarize the feedback for the user:
    - Count of errors vs warnings
    - Most common issue types
    - Files with most issues
    - Estimated effort to fix
  - Ask user if they want to:
    - Continue fixing (proceed with fixes)
    - Fix manually (user will handle it)
    - Skip for now (commit without fixing)

### 5. Commit fixes and push/sync
- After addressing linter feedback (or if skipped):
  - **CRITICAL**: Only stage files that were modified during the fix process
  - Stage fixes: `git add <fixed-files>` (only files that were actually changed by fixes)
  - Commit fixes: `git commit -m "fix: address linter feedback"` (or appropriate message)
  - Push to remote: `git push` (or `git push origin <branch>` if not on main)
  - If push fails (e.g., remote has new commits), inform user and suggest `git pull --rebase` or `git fetch && git rebase origin/main`