# ADR-001: Adopt a Modular Monolith Architecture

**Status:** Accepted

**Date:** 2026-02-14

---

## Context

UnityMatch is a modern AI-powered matrimonial platform that will initially be developed by a small team.

The platform is expected to grow significantly over time and may eventually require independently scalable services such as Chat, Notifications, Search, AI Matching, Payments, and Analytics.

Starting directly with microservices would introduce unnecessary operational complexity, deployment overhead, distributed transactions, and increased development effort for the MVP.

The architecture should therefore support rapid feature development while allowing future migration to microservices with minimal refactoring.

---

## Decision

UnityMatch backend will use a **Modular Monolith** architecture.

Each *business domain* will be implemented as an independent Django application with clearly defined boundaries.

Examples include:

- users
- profiles
- discovery
- interests
- matches
- chat

Business logic will reside in service classes instead of views.

Communication between modules should occur through service interfaces rather than direct model manipulation whenever practical.

---

## Alternatives Considered

### 1. Traditional Django Monolith

Pros

- Simple

Cons

- Business logic easily becomes tightly coupled.
- Difficult to extract services later.

Rejected.

---

### 2. Microservices

Pros

- Independent deployments
- Independent scaling

Cons

- High operational complexity
- Service discovery
- Distributed debugging
- Event consistency
- CI/CD complexity

Rejected for MVP.

---

### 3. Modular Monolith

Pros

- Clear separation of domains
- Easy development
- Simple deployment
- Easier future extraction

Selected.

---

## Consequences

### Positive

- Faster development
- Easier testing
- Single deployment
- Lower infrastructure cost
- Future microservice migration is possible

### Negative

- Entire application scales together.
- Requires discipline to maintain module boundaries.

---

## Future Considerations

Potential future candidates for extraction include:

- Chat
- Notifications
- AI Matching
- Search
- Payments

Extraction will occur only when justified by business or scaling requirements.

---

## References

Architecture documentation.
Backend Engineering Standards.