---
phase: 02-conteneurisation
plan: 01
subsystem: database
tags: [sqlalchemy, alembic, postgresql, python, fastapi]

requires: []
provides:
  - Schéma PostgreSQL forum (4 tables versionnées via Alembic)
  - Modèles SQLAlchemy : User, Category, Topic, Post
  - Couche database.py avec engine, SessionLocal, get_db()
affects: [02-02-api-crud, 02-03-dockerfile-api, 02-04-postgres-network]

tech-stack:
  added: [fastapi==0.111.0, uvicorn, sqlalchemy==2.0.30, alembic==1.13.1, psycopg2-binary, python-dotenv, passlib[bcrypt], python-jose]
  patterns: [declarative_base SQLAlchemy, get_db() generator FastAPI, migrations Alembic versionnées]

key-files:
  created: [src/db/database.py, src/models/user.py, src/models/category.py, src/models/topic.py, src/models/post.py, alembic/versions/001_initial_schema.py]
  modified: []

key-decisions:
  - "Migration écrite manuellement (pas de PostgreSQL live en S2 — validé en 02-04)"
  - "DATABASE_URL exclusivement via os.getenv — aucune valeur hardcodée"

patterns-established:
  - "Tous les modèles héritent de Base (src.db.database)"
  - "src/models/__init__.py importe les 4 modèles pour que Alembic détecte Base.metadata"
  - "downgrade() drop dans l'ordre inverse des FK"

duration: ~30min
started: 2026-06-03T00:00:00Z
completed: 2026-06-03T00:00:00Z
---

# Phase 2 Plan 01 : Schéma DB + Modèles SQLAlchemy + Migration Alembic

**Schéma PostgreSQL forum créé (users, categories, topics, posts) avec modèles SQLAlchemy et migration Alembic initiale reproductible.**

## Performance

| Métrique | Valeur |
|----------|--------|
| Durée | ~30 min |
| Tâches | 3 complètes |
| Fichiers créés | 13 |
| Commits | 2 |

## Acceptance Criteria Results

| Critère | Statut | Notes |
|---------|--------|-------|
| AC-1 : Structure Python initialisée | Pass | `from src.db.database import Base, engine, get_db` → OK |
| AC-2 : Modèles SQLAlchemy cohérents | Pass | `from src.models import User, Category, Topic, Post` → tables : users, categories, topics, posts |
| AC-3 : Migration Alembic applicable | Partial | Migration écrite manuellement — `alembic upgrade head` à valider en 02-04 (PostgreSQL live) |
| AC-4 : Aucun secret versionné | Pass | `git diff` vérifié avant chaque commit — DATABASE_URL uniquement via env |

## Accomplissements

- Couche DB complète : engine, session, base déclarative, générateur `get_db()`
- 4 modèles SQLAlchemy avec contraintes FK et relations (category, author, topic)
- Migration initiale avec `upgrade()` + `downgrade()` dans l'ordre correct des dépendances

## Task Commits

| Tâche | Commit | Type | Description |
|-------|--------|------|-------------|
| T1 — Structure Python + Alembic | `0c97a5b` | chore | initialiser la structure Python, SQLAlchemy et Alembic |
| T2+T3 — Modèles + migration | `7274c52` | feat | ajouter les 4 modèles SQLAlchemy et la migration initiale Alembic |

## Fichiers Créés

| Fichier | Rôle |
|---------|------|
| `requirements.txt` | Dépendances Python versionnées |
| `src/__init__.py` | Package src |
| `src/db/__init__.py` | Package db |
| `src/db/database.py` | engine, SessionLocal, Base, get_db() |
| `src/models/__init__.py` | Import des 4 modèles (détection Alembic) |
| `src/models/user.py` | Table users |
| `src/models/category.py` | Table categories |
| `src/models/topic.py` | Table topics (FK → categories, users) |
| `src/models/post.py` | Table posts (FK → topics, users) |
| `alembic.ini` | Config Alembic |
| `alembic/env.py` | Env Alembic (DATABASE_URL via os.environ) |
| `alembic/script.py.mako` | Template migration |
| `alembic/versions/001_initial_schema.py` | Migration initiale |

## Déviations

| Type | Description | Impact |
|------|-------------|--------|
| DONE_WITH_CONCERNS | Migration écrite manuellement (pas `--autogenerate`) — PostgreSQL absent | Faible — même résultat, validé en 02-04 |

## Next Phase Readiness

**Prêt :**
- Modèles importables et utilisables par 02-02 (API CRUD)
- `get_db()` prêt comme dépendance FastAPI
- Migration prête à tourner dès PostgreSQL disponible (02-04)

**Concerns :**
- `alembic upgrade head` non testé — dépend de 02-04 (Lead Ops)

**Blockers :** Aucun pour 02-02

---
*Phase: 02-conteneurisation, Plan: 01*
*Completed: 2026-06-03*
