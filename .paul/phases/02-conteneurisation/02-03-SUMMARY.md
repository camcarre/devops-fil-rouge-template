---
phase: 02-conteneurisation
plan: 03
subsystem: infra
tags: [docker, dockerfile, multi-stage, python-slim]

requires:
  - phase: 02-02
    provides: src/main.py entry point, requirements.txt, src/routers/

provides:
  - Dockerfile multi-stage (builder + runtime python:3.12-slim)
  - .dockerignore (exclut .env, __pycache__, .venv, .git, .paul)
  - Image forum-api buildable et fonctionnelle

affects: [02-04-postgres-network, 03-01-docker-compose, 03-03-ci-workflow]

tech-stack:
  added: [python:3.12-slim, multi-stage build]
  patterns: [pip install --prefix=/install pour isoler les dépendances du builder]

key-files:
  created:
    - Dockerfile
    - .dockerignore

key-decisions:
  - "PYTHONPATH=/app requis — uvicorn ne l'ajoute pas automatiquement au sys.path"
  - "Multi-stage builder/runtime — dépendances installées dans /install, copiées dans /usr/local"
  - "CMD via sh -c pour substitution de variable PORT au runtime"

patterns-established:
  - "IMAGE_NAME=forum-api pour toutes les références CI/docker-compose suivantes"
  - "Secrets DATABASE_URL + SECRET_KEY injectés au runtime uniquement (valeur vide dans image)"

duration: ~25min
started: 2026-06-04T00:00:00Z
completed: 2026-06-04T00:00:00Z
---

# Phase 2 Plan 03: Dockerfile Summary

**Image Docker multi-stage python:3.12-slim buildée et validée : `docker build -t forum-api .` + GET /health → {"status":"ok"} depuis le container.**

## Performance

| Metric | Value |
|--------|-------|
| Duration | ~25min |
| Tasks | 2/2 complétés |
| Files créés | 2 |

## Acceptance Criteria Results

| Criterion | Status | Notes |
|-----------|--------|-------|
| AC-1: Image se build sans erreur | Pass | `docker build -t forum-api .` exit 0 |
| AC-2: Container démarre et /health répond | Pass | `{"status":"ok"}` confirmé |
| AC-3: Aucun secret dans l'image | Pass | DATABASE_URL="" SECRET_KEY="" — valeurs vides, runtime only |

## Accomplishments

- Image multi-stage : builder installe les deps, runtime ne contient que le nécessaire
- Container démarre sans DB réelle grâce au lazy connect de SQLAlchemy
- .dockerignore protège .env et .paul du contexte de build

## Files Created

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage builder + runtime, PYTHONPATH=/app, CMD uvicorn |
| `.dockerignore` | Exclut .env, __pycache__, .venv, .git, .paul, docs |

## Decisions Made

| Decision | Rationale | Impact |
|----------|-----------|--------|
| `PYTHONPATH=/app` dans ENV | uvicorn ne met pas le WORKDIR dans sys.path automatiquement | Requis pour que `src.main` soit importable |
| `pip install --prefix=/install` | Sépare dépendances du builder du runtime | Image runtime allégée sans outils de build |
| `sh -c "uvicorn ... --port ${PORT}"` | Substitution de variable d'env dans CMD | PORT configurable au runtime sans rebuild |

## Deviations from Plan

| Type | Description | Impact |
|------|-------------|--------|
| Auto-fix | Ajout `PYTHONPATH=/app` non prévu dans le plan initial | Essentiel — sans ça `src.main` non importable |
| Contexte | Merge de feature/02-02-api-crud nécessaire (src/main.py absent sur 02-03) | Normal — branche 02-03 créée avant 02-02 mergé sur master |

## Next Phase Readiness

**Ready:**
- `docker build -t forum-api .` documenté et fonctionnel
- Image name `forum-api` à utiliser dans docker-compose (02-04) et CI (03-03)
- Pas de secret hardcodé : injection DATABASE_URL + SECRET_KEY via `docker run -e`

**Blockers:** None — 02-04 (PostgreSQL + réseau Docker) peut démarrer.

---
*Phase: 02-conteneurisation, Plan: 03*
*Completed: 2026-06-04*
