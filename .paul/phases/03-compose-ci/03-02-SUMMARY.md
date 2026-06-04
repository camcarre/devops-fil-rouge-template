---
phase: 03-compose-ci
plan: 02
type: execute
status: done
owner: Lead Qualité / CI (Camille Douaud)
completed: 2026-06-04
---

# SUMMARY 03-02 — Tests automatisés (unit + smoke API)

## Objectif
Couvrir l'API forum (FastAPI) par une suite de tests automatisés exécutable en local et en CI (préparation 03-03).

## Réalisé
- `tests/conftest.py` : fixtures pytest — moteur **SQLite en mémoire** (`StaticPool`, connexion partagée), override de `get_db`, `TestClient` FastAPI, fixtures `auth_token` / `auth_headers` (auth JWT **réelle**, aucun mock sur DB/auth).
- `tests/test_health.py` : smoke `GET /health`.
- `tests/test_auth.py` : register 201, email dupliqué 400, login 200 + token bearer, mauvais mot de passe 401, email inconnu 401, vérif mot de passe **haché** en DB (préfixe `$2`, jamais en clair).
- `tests/test_forum.py` : catégories (liste publique, création protégée 401 sans token / 201 avec), topics (404 catégorie inconnue, création+liste, 401 sans token), posts (404 topic inconnu, création+liste, 401 sans token).
- `pytest.ini` : `pythonpath = .`, `testpaths = tests`.
- `requirements-dev.txt` : `-r requirements.txt` + `pytest==8.2.0` + `httpx==0.27.0`.

## Vérification
```
python3 -m pytest -q
17 passed in 6.31s
```

## Couverture fonctionnelle
| Domaine | Cas testés |
|---------|-----------|
| Health | 1 (smoke) |
| Auth | 6 (register, dup, login, bad pw, unknown, hash en DB) |
| Forum CRUD | 10 (catégories / topics / posts : public, protégé, 404, listing) |

## Décisions
- **SQLite in-memory** plutôt que Postgres pour les tests : rapide, sans dépendance réseau, suffisant (aucun type Postgres-spécifique dans les modèles). Le smoke api↔db Postgres reste couvert par le compose (02-04).
- **Auth réelle** (register → login → token) au lieu d'un override de `get_current_user` : teste le vrai chemin JWT + bcrypt (cf. CONVENTIONS « pas de mocks pour DB/auth si vraie intégration faisable »).

## Suites
- 03-03 : workflow GitHub Actions exécutant `pip install -r requirements-dev.txt && pytest`.

## Notes / dette
- `src/security.py:30` et défauts modèles utilisent `datetime.utcnow()` (déprécié Python 3.12+) → warnings non bloquants. À migrer vers `datetime.now(datetime.UTC)` (hors scope 03-02, candidat fix futur).
