---
phase: 02-conteneurisation
plan: 04
subsystem: infra
tags: [docker-compose, postgres, alembic, réseau-docker, healthcheck]

requires:
  - phase: 02-03
    provides: Dockerfile buildable, image forum-api

provides:
  - docker-compose.yml (api + db + réseau + volume + healthcheck)
  - Stack reproductible via `docker-compose up`
  - Migrations Alembic auto au démarrage api

affects: [03-01-docker-compose, 03-03-ci-workflow, 04-01-k8s-cluster]

tech-stack:
  added: [postgres:16-alpine, docker-compose networks, named volumes]
  patterns: [depends_on condition:service_healthy, alembic upgrade head au démarrage]

key-files:
  created:
    - docker-compose.yml
  modified:
    - .env.example (ajout POSTGRES_USER/PASSWORD/DB)
    - src/security.py (passlib → bcrypt direct)

key-decisions:
  - "bcrypt direct au lieu de passlib — incompatibilité passlib 1.7.4 + bcrypt 5.x"
  - "depends_on condition:service_healthy — attend pg_isready avant de démarrer l'api"
  - "alembic upgrade head dans le CMD api — migrations auto sans step manuel"

patterns-established:
  - "Réseau = forum-network (bridge), nom DNS interne db → PostgreSQL"
  - "Volume nommé postgres-data pour la persistance entre restarts"
  - "Variables injectées via .env (jamais en clair dans docker-compose.yml)"

duration: ~30min
started: 2026-06-04T00:00:00Z
completed: 2026-06-04T00:00:00Z
---

# Phase 2 Plan 04: docker-compose + PostgreSQL Summary

**Stack forum reproductible en une commande `docker-compose up` : api FastAPI + PostgreSQL 16, réseau Docker, migrations Alembic auto, smoke test POST /auth/register → user persisté en DB.**

## Performance

| Metric | Value |
|--------|-------|
| Duration | ~30min |
| Tasks | 2/2 complétés |
| Files créés/modifiés | 3 |

## Acceptance Criteria Results

| Criterion | Status | Notes |
|-----------|--------|-------|
| AC-1: Stack démarre avec docker-compose up | Pass | api + db running, docker-compose ps confirmed |
| AC-2: API connectée à PostgreSQL | Pass | POST /auth/register → 201, user dans DB |
| AC-3: Migrations Alembic au démarrage | Pass | 5 tables (4 + alembic_version) dans psql \dt |
| AC-4: Aucun secret dans docker-compose.yml | Pass | Uniquement ${VAR}, .env dans .gitignore |

## Accomplishments

- `docker-compose up` fonctionnel en une commande depuis `.env`
- Healthcheck PostgreSQL (pg_isready) bloque l'API jusqu'à ce que la DB soit prête
- User créé via register persiste entre restarts grâce au volume nommé

## Files Created/Modified

| File | Change | Purpose |
|------|--------|---------|
| `docker-compose.yml` | Créé | Services api + db, réseau forum-network, volume postgres-data |
| `.env.example` | Modifié | Ajout POSTGRES_USER/PASSWORD/DB |
| `src/security.py` | Modifié | Remplacement passlib par bcrypt direct (fix compat) |

## Decisions Made

| Decision | Rationale | Impact |
|----------|-----------|--------|
| bcrypt direct (sans passlib) | passlib 1.7.4 lève ValueError avec bcrypt >= 4.x lors de l'init | hash_password et verify_password fonctionnels en container |
| `alembic upgrade head` dans CMD | Migrations auto sans intervention manuelle | Simplifie le déploiement (K8s aussi) |
| `condition: service_healthy` | Evite les race conditions api/db au démarrage | Fiable même sur machine lente |

## Deviations from Plan

| Type | Description | Impact |
|------|-------------|--------|
| Auto-fix | src/security.py modifié (hors boundary 02-02) | Nécessaire — bug bloquant incompatibilité passlib/bcrypt |

## Next Phase Readiness

**Ready:**
- `docker-compose up` documenté et validé — référence pour la CI (03-01/03-03)
- `docker-compose.yml` utilisable tel quel en Phase 3 avec ajout healthchecks applicatifs
- Secrets via `.env` → pattern réutilisable pour GitHub Secrets (03-04)

**Phase 2 COMPLÈTE — prêt pour Phase 3 (docker-compose + CI verte)**

**Blockers:** None.

---
*Phase: 02-conteneurisation, Plan: 04*
*Completed: 2026-06-04*
