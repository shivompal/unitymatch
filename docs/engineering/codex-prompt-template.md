# Standard Prompt

Follow UnityMatch Backend Engineering Standards.

Before writing code:

- Preserve the Modular Monolith architecture.
- Keep views thin.
- Place business logic in services/.
- Never create services.py.
- Use UUIDs everywhere.
- Validate ownership and permissions.
- Use select_related()/prefetch_related() where appropriate.
- Write tests for new features.
- Do not introduce new dependencies unless requested.
- Reuse existing project conventions instead of creating new patterns.
- If an architectural decision is unclear, do not guess—leave a note for review.
- If a requested implementation conflicts with the engineering standards,
  follow the standards and explain the conflict.