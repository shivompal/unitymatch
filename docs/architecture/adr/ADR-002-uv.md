# ADR-002: Adopt uv as the Python Package Manager

**Status:** Accepted

**Date:** 2026-02-14

---

## Context

Python projects traditionally use pip together with requirements.txt.

UnityMatch requires:

- reproducible builds
- fast dependency installation
- dependency locking
- virtual environment management
- Docker compatibility
- CI/CD compatibility

A modern dependency manager better satisfies these requirements.

---

## Decision

UnityMatch will use **uv** for dependency management.

Project files include:

- pyproject.toml
- uv.lock

requirements.txt will not be maintained.

Virtual environments will be managed using uv.

---

## Alternatives Considered

### pip + requirements.txt

Pros

- Universally supported

Cons

- Slower
- Separate lock management
- Less modern workflow

Rejected.

---

### Pipenv

Pros

- Lock file
- Virtual environments

Cons

- Slower than uv
- Less active ecosystem momentum

Rejected.

---

### Poetry

Pros

- Mature
- Feature rich

Cons

- Additional complexity
- Slower dependency resolution

Rejected.

---

### uv

Pros

- Extremely fast
- Lock file
- Virtual environments
- Modern packaging
- Excellent Docker support

Selected.

---

## Consequences

### Positive

- Faster dependency installation
- Faster CI
- Faster Docker builds
- Reproducible environments

### Negative

- Some developers may be unfamiliar with uv.
- Team documentation is required.

---

## Future Considerations

Development dependency groups will be introduced for:

- Ruff
- Pytest
- Mypy
- Pre-commit

---

## References

https://docs.astral.sh/uv/