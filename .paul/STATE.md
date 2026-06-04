# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-06-03)

**Core value:** Maîtrise DevOps de bout en bout (code conteneurisé → K8s monitoré) sur un forum simple, reproductible via `docker-compose up`.
**Current focus:** v0.1 Fil Rouge — Phase 5 (S5 Monitoring + scan + post-mortem) COMPLETE — prêt pour Phase 6

## Current Position

Milestone: v0.1 Fil Rouge (S1→S6)
Phase: 5 of 6 (S5 — Monitoring + scan + post-mortem) — COMPLETE
Plan: 05-01→05-04 DONE — Phase 5 terminée ; next Phase 6 (Soutenance)
Status: Phase 5 COMPLETE (Lead Produit / Doc)
Last activity: 2026-06-04 — Phase 5 : metrics endpoint, Prometheus instrumentation, Grafana dashboards, scan Trivy + audit dépendances, post-mortem rédigé

Progress:
- Milestone: [████████░] 83% (Phase 1 + 2 + 3 + 4 + 5 done)
- Phase 5: [██████████] 100% (05-01 metrics + 05-02 Grafana + 05-03 security scan + 05-04 postmortem)

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
Stopped at: Phase 4 complète (Lead Ops) — manifests k8s/ déployés et vérifiés, PR #9 ouverte vers master
Next action: faire relire/merger PR #9, puis Phase 5 (Monitoring) → /metrics, Prometheus, Grafana (addons minikube)
Resume context: cluster minikube profile=forum, namespace=forum. Manifests dans k8s/ (00→30). Image API chargée via `minikube image load`. Accès : port-forward svc/api ou `minikube tunnel` + forum.local. Vrai secret k8s/02-secret.yaml gitignoré.

---
*STATE.md — Updated after every significant action*
*Size target: <100 lines (digest, not archive)*
