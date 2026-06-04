---
phase: 03-compose-ci
plan: 04
type: execute
status: done
owner: Lead Qualité / CI (Camille Douaud)
completed: 2026-06-04
---

# SUMMARY 03-04 — GitHub Secrets + consommateur CI

## Objectif
Injecter les secrets via **GitHub Secrets** (jamais en clair) et les faire réellement consommer par la CI.

## Réalisé
- **4 GitHub Secrets** configurés (`gh secret set`, valeurs générées non affichées) :
  - `SECRET_KEY` (aléatoire, `secrets.token_hex(32)`)
  - `POSTGRES_PASSWORD` (aléatoire, `secrets.token_hex(16)`)
  - `POSTGRES_USER` = `forum_user`
  - `POSTGRES_DB` = `forum`
- **Job CI `integration`** (`.github/workflows/ci.yml`, `needs: lint-test`) qui consomme les secrets :
  - Génère un `.env` depuis les secrets (mapping `env:`, jamais en dur dans `run:`)
  - `docker compose up -d --build`
  - Poll `GET /health` (30 essais × 3 s)
  - `docker compose down -v` (teardown `if: always()`)
  - Remplace l'ancien job `build` (le build d'image est inclus dans `compose up --build`).
- `.env.example` : déjà aligné sur toutes les vars compose (`POSTGRES_*`, `SECRET_KEY`, `PORT`, `DATABASE_URL`) — aucun changement nécessaire. Édition bloquée par la règle sécu `.env*` de toute façon.

## Sécurité
- Secrets stockés chiffrés côté GitHub, jamais commités.
- Injection via `env:` (pas d'interpolation `${{ }}` dans les `run:`) → pas de command injection.
- GitHub masque automatiquement les valeurs de secrets dans les logs.

## Vérification
- Validation = run GitHub Actions vert (lint-test + integration), `/health` répond depuis le conteneur api alimenté par les secrets.

## Clôture Phase 3
Tous les plans 03-xx terminés → **Phase 3 (S3 — docker-compose + CI verte) complète**.
