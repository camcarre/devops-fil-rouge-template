---
phase: 02-conteneurisation
plan: 02
subsystem: api
tags: [fastapi, jwt, bcrypt, pydantic, sqlalchemy]

requires:
  - phase: 02-01
    provides: SQLAlchemy models (User, Category, Topic, Post) + DB session + Alembic migrations

provides:
  - API FastAPI importable et structurée (src/main.py)
  - Auth JWT register/login (src/routers/auth.py)
  - CRUD catégories/topics/posts protégé par token (src/routers/)
  - Utilitaires sécurité (src/security.py)
  - Schemas Pydantic request/response (src/schemas.py)

affects: [02-03-dockerfile, 03-02-tests, 03-03-ci-workflow]

tech-stack:
  added: [passlib[bcrypt], python-jose[cryptography]]
  patterns: [OAuth2PasswordBearer, Depends injection, router prefix]

key-files:
  created:
    - src/main.py
    - src/security.py
    - src/schemas.py
    - src/routers/__init__.py
    - src/routers/auth.py
    - src/routers/categories.py
    - src/routers/topics.py
    - src/routers/posts.py

key-decisions:
  - "Pydantic v2 ConfigDict(from_attributes=True) plutôt que orm_mode — FastAPI 0.111.0 cible pydantic v2"
  - "OAuth2PasswordRequestForm : username = email (convention forum)"
  - "SECRET_KEY via os.getenv uniquement — jamais hardcodé"

patterns-established:
  - "Toutes les routes POST de création sont protégées par Depends(get_current_user)"
  - "Routes publiques = GET listes, routes protégées = POST création"
  - "404 systématique si ressource parente inexistante (category, topic)"

duration: ~20min
started: 2026-06-04T00:00:00Z
completed: 2026-06-04T00:00:00Z
---

# Phase 2 Plan 02: API CRUD + Auth JWT Summary

**API FastAPI Forum opérationnelle : auth JWT (register/login bcrypt) + 6 routes CRUD catégories/topics/posts prêtes pour conteneurisation.**

## Performance

| Metric | Value |
|--------|-------|
| Duration | ~20min |
| Tasks | 3/3 complétés |
| Files créés | 8 |

## Acceptance Criteria Results

| Criterion | Status | Notes |
|-----------|--------|-------|
| AC-1: App FastAPI démarre | Pass | `from src.main import app` sans erreur, /health déclaré |
| AC-2: Auth register/login fonctionnel | Pass | Routes /auth/register et /auth/login déclarées, bcrypt + JWT |
| AC-3: Routes CRUD forum protégées | Pass | 6 routes (GET public, POST protégé), 401 sans token |
| AC-4: Aucun secret versionné | Pass | SECRET_KEY et DATABASE_URL via os.getenv uniquement |

## Accomplishments

- Auth JWT complète : hash bcrypt via passlib, tokens signés via python-jose
- 8 fichiers créés couvrant l'intégralité de la couche applicative
- Structure router modulaire prête à être conteneurisée en 02-03

## Files Created

| File | Purpose |
|------|---------|
| `src/main.py` | Entry point FastAPI, montage des 4 routers, GET /health |
| `src/security.py` | hash_password, verify_password, create_access_token, get_current_user |
| `src/schemas.py` | Pydantic v2 : UserCreate/Out, Token, CategoryCreate/Out, TopicCreate/Out, PostCreate/Out |
| `src/routers/__init__.py` | Package marker |
| `src/routers/auth.py` | POST /auth/register (201), POST /auth/login |
| `src/routers/categories.py` | GET /categories/, POST /categories/ (protégé) |
| `src/routers/topics.py` | GET + POST /categories/{id}/topics (POST protégé) |
| `src/routers/posts.py` | GET + POST /topics/{id}/posts (POST protégé) |

## Decisions Made

| Decision | Rationale | Impact |
|----------|-----------|--------|
| Pydantic v2 `ConfigDict(from_attributes=True)` | FastAPI 0.111.0 cible pydantic v2 | Évite DeprecationWarning sur `orm_mode` |
| `form.username` = email au login | OAuth2PasswordRequestForm impose le champ `username` | Convention documentée dans schemas |

## Deviations from Plan

None — plan exécuté tel que spécifié.

## Next Phase Readiness

**Ready:**
- `src/main.py` + `src/routers/` : entry point connu pour le Dockerfile (`uvicorn src.main:app`)
- `requirements.txt` déjà présent avec toutes les dépendances
- Pas de secret hardcodé : injection via `.env` compatible Docker

**Blockers:** None — 02-03 (Dockerfile) peut démarrer.

---
*Phase: 02-conteneurisation, Plan: 02*
*Completed: 2026-06-04*
