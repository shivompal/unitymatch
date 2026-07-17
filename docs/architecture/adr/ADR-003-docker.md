# ADR-003: Adopt Docker for Local Development

**Status:** Accepted

**Date:** 2026-07-16

---

## Context

Developers frequently experience differences in local environments due to:

- Python versions
- PostgreSQL versions
- Redis versions
- Operating systems
- Package conflicts

The project requires a consistent development environment that is also suitable for CI/CD and future production deployment.

---

## Decision

UnityMatch will use Docker Compose for local development.

The development stack consists of:

- Django Backend
- PostgreSQL 18
- Redis

Official Docker images will be used for PostgreSQL and Redis.

Only the backend image will have a custom Dockerfile.

Docker files will be organized as:

docker/
    backend/
        Dockerfile

A single docker-compose.yml at the repository root will *orchestrate* all services.

---

## Alternatives Considered

### Native Installation

Pros

- No Docker knowledge required

Cons

- Environment inconsistencies
- Difficult onboarding
- Version drift

Rejected.

---

### Docker for Backend Only

Pros

- Partial isolation

Cons

- PostgreSQL and Redis remain inconsistent

Rejected.

---

### Full Docker Compose

Pros

- Consistent environments
- Simple onboarding
- Easy CI integration
- Production similarity

Selected.

---

## Consequences

### Positive

- Identical environments
- Easier onboarding
- Reproducible builds
- Better CI/CD support

### Negative

- Docker learning curve
- Slightly higher resource usage

---

## Future Considerations

Future services may include:

- Elasticsearch
- Celery
- Celery Beat
- Nginx

These will be added to Docker Compose when required.

Production deployment may later use:

- Docker Swarm
- Kubernetes

This decision does not require Kubernetes for the MVP.

---

## References

Docker documentation.

Docker Compose documentation.