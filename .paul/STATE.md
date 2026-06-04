# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-06-03)

**Core value:** Maîtrise DevOps de bout en bout (code conteneurisé → K8s monitoré) sur un forum simple, reproductible via `docker-compose up`.
**Current focus:** v0.1 Fil Rouge — Phase 5 (S5 Monitoring + scan + post-mortem) COMPLETE — prêt pour Phase 6

## Current Position

Milestone: v0.1 Fil Rouge (S1→S6)
Phase: 6 of 6 (S6 — Soutenance) — In Progress
Plan: 06-01 COMPLETE — loop fermé ; next 06-02 (répétition démo) + 06-03 (slides)
Status: Ready for next PLAN (06-02)
Last activity: 2026-06-04 — UNIFY 06-01 : docs/architecture.md + README + k8s/README.md livrés

Progress:
- Milestone: [█████████░] 90% (Phase 1→5 done, Phase 6 en cours)
- Phase 6: [████░░░░░░] 33% (06-01 ✓, 06-02 et 06-03 restants)

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓     [06-01 loop fermé — prêt pour 06-02]
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
| minikube (vs kind) | S4 | Addons intégrés (ingress, metrics-server) pour S4/S5 |
| StatefulSet+PVC db / Deployment api | S4 | DB persistante stable, API stateless scalable |
| Migration en initContainer | S4 | `alembic upgrade head` avant démarrage uvicorn |
| Secret K8s gitignoré + gabarit examples/ | S4 | Aucun secret versionné, apply -f k8s/ sûr |

### Deferred Issues

None.

### Blockers/Concerns

None.

## Boundaries (Active)

Aucune restriction — code applicatif autorisé.

## Session Continuity

Last session: 2026-06-04
Stopped at: UNIFY 06-01 complet
Next action: `/paul:plan` → Phase 6 plan 06-02 (répétition démo bout-en-bout) et 06-03 (slides soutenance)
Resume context: docs livrées (architecture.md 132L, README TODO:, k8s/README démo). Placeholders README à compléter par l'équipe. Plans 06-02 et 06-03 restants.

---
*STATE.md — Updated after every significant action*
*Size target: <100 lines (digest, not archive)*
