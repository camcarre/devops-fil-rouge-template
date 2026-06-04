---
phase: 03-compose-ci
plan: 03
type: execute
status: done
owner: Lead Qualité / CI (Camille Douaud)
completed: 2026-06-04
---

# SUMMARY 03-03 — Workflow GitHub Actions (lint + test + build)

## Objectif
Pipeline CI **vert** déclenché sur push et PR vers `master` : lint + tests + build de l'image.

## Réalisé
- `.github/workflows/ci.yml` :
  - Triggers : `push` et `pull_request` sur `master`.
  - Job **lint-test** : checkout, setup Python 3.12 (cache pip), `pip install -r requirements-dev.txt`, `ruff check src tests`, `pytest -q` (env `DATABASE_URL=sqlite://`, `SECRET_KEY=ci-test-secret`).
  - Job **build** (`needs: lint-test`) : `docker build -t forum-api:ci .` — valide le Dockerfile.
- `ruff.toml` : `line-length=100`, règles `E`/`F`/`I`, ignore `E402` dans `tests/conftest.py` (env avant imports).
- `requirements-dev.txt` : ajout `ruff==0.4.4`.
- `README.md` : badge CI.

## Sécurité
- Aucun input non fiable (`github.event.*`) injecté dans les `run:` → pas de risque d'injection de commande.
- Aucun secret en clair : les valeurs de test CI sont factices ; les vrais secrets passeront par GitHub Secrets (03-04).

## Vérification (locale, avant push)
```
ruff check src tests   → All checks passed!
pytest -q              → 17 passed
```
Validation finale = run GitHub Actions vert sur la PR.

## Suites
- 03-04 : configurer les GitHub Secrets + aligner `.env.example`.

## Notes
- ruff pinné `0.4.4` dans requirements-dev (local utilisé : 0.15.12, config compatible).
