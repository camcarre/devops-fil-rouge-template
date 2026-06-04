# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-06-03)

**Core value:** Maîtrise DevOps de bout en bout (code conteneurisé → K8s monitoré) sur un forum simple, reproductible via `docker-compose up`.
**Current focus:** v0.1 Fil Rouge — Phase 3 (S3 docker-compose + CI verte)

## Current Position

Milestone: v0.1 Fil Rouge (S1→S6)
Phase: 3 of 6 (S3 — docker-compose + CI verte)
Plan: Phase 2 COMPLÈTE — prêt pour Phase 3
Status: Ready to plan 03-01
Last activity: 2026-06-04 — Phase 2 terminée : docker-compose up fonctionnel, api↔db validé

Progress:
- Milestone: [████░░░░░░] 33% (Phase 1 + 2 done)
- Phase 3: [░░░░░░░░░░] 0%

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓     [Phase 2 terminée — prêt pour Phase 3]
```

## Accumulated Context

### Decisions

| Decision | Phase | Impact |
|----------|-------|--------|
| Forum comme sujet (API + DB) | S1 | Cadre les features minimales |
| Monolithe + PostgreSQL | S1 | Architecture de référence pour toutes les phases |
| Pas de temps réel ni OAuth | S1 | Périmètre minimal intentionnel |
| Stack Python FastAPI | S2 | Entry point = `uvicorn src.main:app` |
| PYTHONPATH=/app dans Dockerfile | S2 | uvicorn ne met pas WORKDIR dans sys.path auto |
| Image name = forum-api | S2 | Référence pour docker-compose et CI |
| bcrypt direct (sans passlib) | S2 | Incompatibilité passlib 1.7.4 + bcrypt 5.x |
| alembic upgrade head dans CMD api | S2 | Migrations auto au démarrage, sans intervention |
| Réseau = forum-network, DNS interne = db | S2 | DATABASE_URL utilise `db` comme hostname |

### Deferred Issues

None.

### Blockers/Concerns

None.

## Boundaries (Active)

Aucune restriction — code applicatif autorisé.

## Session Continuity

Last session: 2026-06-04
Stopped at: Phase 2 complète mergée sur master — Lead Dev a terminé son périmètre
Next action: Lead CI/CD → `/paul:plan` Phase 3 sur feature/03-01-docker-compose
Resume context: `docker-compose up` validé localement. Image=forum-api, réseau=forum-network, DB=postgres:16-alpine. Migrations auto (alembic upgrade head). Secrets via .env → pattern GitHub Secrets pour la CI.

---
*STATE.md — Updated after every significant action*
*Size target: <100 lines (digest, not archive)*
