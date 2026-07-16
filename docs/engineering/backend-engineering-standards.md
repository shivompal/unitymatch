# UnityMatch Backend Engineering Standards

**Version:** 1.0  
**Status:** Active  
**Last Updated:** July 2026

**Owner:** Shiv Om Pal

**Architectural Guide:** ChatGPT

**Applies To:** `backend/`

---

## Version History

| Version | Date | Changes |
|----------|------|---------|
| 1.0 | July 2026 | Initial engineering standards |

---

# Purpose

This document defines the engineering standards for the UnityMatch backend.

Its goals are to:

- Maintain consistency
- Improve readability
- Simplify onboarding
- Guide AI coding assistants (Codex)
- Enable long-term scalability

> Whenever there is a conflict between convenience and consistency, **consistency wins**.

---

# Engineering Principles

UnityMatch follows these principles:

- Keep it simple.
- Security by default.
- Explicit is better than implicit.
- Business logic belongs in the service layer.
- APIs should be predictable.
- Optimize for maintainability over cleverness.

---

# Repository Architecture

UnityMatch uses a **Monorepo**.

```text
unitymatch/

├── backend/
├── frontend/
├── docs/
├── .agents/
├── .codex/
└── README.md
```

---

# Backend Architecture

The backend follows a **Modular Monolith** architecture.

Each Django application represents an independent business domain.

```text
apps/

├── users/
├── profiles/
├── interests/
├── matches/
├── discovery/
└── chat/
```

Each module should be independently maintainable.

---

# Standard Django App Structure

Every Django application should follow this structure.

```text
app_name/

├── migrations/
├── services/
│   └── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── urls.py
├── views.py
└── tests.py
```

### Optional modules

```text
permissions.py
validators.py
selectors.py
tasks.py
signals.py
```

### Rules

❌ Never create

```text
services.py
```

✅ Always use

```text
services/
```

---

# Service Layer

Business workflows belong inside the service layer.

Examples:

- `accept_interest()`
- `reject_interest()`
- `create_match()`
- `create_chat_room()`
- `upload_photo()`
- `set_primary_photo()`

### Rules

- Services may call models.
- Views should call services.
- Services should not depend on HTTP requests.

---

# Views

Views should remain **thin**.

Responsibilities:

- Authentication
- Authorization
- Input validation
- Calling services
- Returning HTTP responses

Views must **not** contain business workflows.

---

# Serializers

Serializers are responsible for:

- Validation
- Serialization
- Deserialization

Serializers should **not**:

- Create matches
- Create chat rooms
- Send emails
- Perform business workflows

---

# Models

Models should remain lightweight.

Allowed:

- Fields
- `Meta`
- `__str__()`
- Small helper properties

Complex workflows belong in services.

---

# Database Standards

### Primary Keys

Use **UUID** everywhere.

### Constraints

Prefer database constraints over application-only validation whenever possible.

### Indexes

Create indexes for frequently filtered or searched fields.

---

# API Standards

Follow REST principles.

### HTTP Methods

- GET
- POST
- PUT
- PATCH
- DELETE

### HTTP Status Codes

- 200 OK
- 201 Created
- 204 No Content
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

### Rules

- Always validate ownership.
- Never trust IDs supplied by clients.

---

# Security

Every endpoint must answer one question:

> Can this authenticated user perform this action?

Always scope queries using:

```python
request.user
```

Never expose another user's data.

---

# Query Optimization

Always review queryset performance.

Prefer:

```python
select_related()
prefetch_related()
```

Avoid N+1 query problems.

---

# Testing Standards

Every feature should include tests.

Minimum coverage:

- Happy path
- Validation
- Authorization
- Ownership
- Business rules

Regression tests are mandatory for bug fixes.

---

# Git Workflow

Every feature follows this workflow.

```text
Design
    ↓
Implementation
    ↓
Review
    ↓
Testing
    ↓
Commit
    ↓
Push
```

### Commit Messages

Examples:

```text
feat: add profile photo APIs
fix: prevent duplicate interests
refactor: move photo logic to service layer
```

---

# AI-Assisted Development

UnityMatch follows this workflow.

```text
Design
    ↓
Codex
    ↓
ChatGPT Review
    ↓
Testing
    ↓
Commit
    ↓
Push
```

### ChatGPT Responsibilities

- Architecture
- Product decisions
- Security review
- Scalability
- Code review

### Codex Responsibilities

- Boilerplate
- CRUD APIs
- Refactoring
- Tests
- Repetitive implementation

The developer remains responsible for all final decisions.

---

# Product Philosophy

UnityMatch is a **trust-first matrimonial platform**.

Every engineering decision should improve:

- Trust
- Privacy
- Simplicity
- Safety

Avoid hidden automation when explicit user actions provide better clarity.

---

# Scalability Strategy

### Current

```text
Monorepo
        ↓
Modular Monolith
```

### Future

```text
Monorepo
        ↓
Hybrid Architecture
        ↓
Microservices
```

Potential future services:

- Authentication
- Chat
- Notifications
- Discovery
- AI
- Search

Introduce microservices only when there is a demonstrated need for independent scaling, deployment, or ownership.

---

# Definition of Done

A feature is complete only when:

- Architecture approved
- Code reviewed
- Tests added
- API tested
- Documentation updated (if applicable)
- Commit pushed

---

# Coding Standards

- Follow PEP 8.
- Use descriptive names.
- Keep functions focused on one responsibility.
- Prefer readability over clever code.
- Avoid duplicate logic.
- Document non-obvious business rules.

---

# Dependency Management

### Package Manager

```text
uv
```

### Current

```text
requirements.txt
```

### Target (Planned)

```text
pyproject.toml
uv.lock
```

> Migration to the modern `uv` workflow will be completed during the Dockerization milestone.

### Runtime Dependencies

```bash
uv add <package>
```

### Development Dependencies

```bash
uv add --dev <package>
```

Avoid introducing new dependencies unless they provide long-term value.

---

# Docker & Environment

Development environment should use Docker Compose.

### Target Services

- Django
- PostgreSQL 18
- Redis

Configuration must come from environment variables rather than hard-coded values.

---

# Architectural Decisions (ADR)

## ADR-001 — Monorepo

**Decision**

Use a Monorepo.

**Reason**

- Easier refactoring
- Shared documentation
- AI agents have complete project context

---

## ADR-002 — Modular Monolith

**Decision**

Backend architecture is a Modular Monolith.

**Reason**

- Faster MVP development
- Easy migration to microservices
- Single deployment

---

## ADR-003 — Service Layer

**Decision**

Business logic belongs in `services/`.

**Reason**

- Thin views
- Reusable business logic
- Better testing

---

# Engineering Motto

> **Simple. Secure. Consistent. Scalable.**

---

# Founder's Principle

> **We are not just building software. We are building a platform that people can trust with one of the most important decisions of their lives.**