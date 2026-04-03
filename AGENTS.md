# Agent Working Memory

This file captures practical rules learned from recent debugging sessions.
Follow these rules in future tasks for this repository.

## Terminal and Execution Rules

- Always reuse the current Cursor terminal context first.
- Do not spawn extra `cmd /c` wrappers unless explicitly requested.
- For this project, assume the user's current cmd terminal is UTF-8 when they say so.
- If encoding issues appear, prefer minimal command adjustments in the same terminal context.

## Testing Workflow Rules

- Start with the smallest failing scope (`pytest -x <target>`) to locate root cause fast.
- After fixing root cause, rerun the full relevant suite before declaring success.
- Prefer reporting concrete pass/fail counts and failing groups, not generic statements.

## Communication Rules

- Do not ask the user to rerun commands repeatedly when the agent can run them directly.
- When a previous approach was wrong, acknowledge clearly and switch to the requested workflow immediately.
- Keep changes minimal and explicit when the user asks for a "minimum keep set".

## PowerMem-Specific Lessons

- `memory.search` with intelligent memory enabled can trigger lifecycle side effects.
- Distinguish search/ranking logic from deletion behavior when debugging data loss.
- Keep CLI env loading and example env source aligned (same env file path) when validating behavior.

