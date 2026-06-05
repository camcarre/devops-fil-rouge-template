# Note d'architecture — Forum DevOps Fil Rouge

> Application de forum (catégories → sujets → messages) livrée par une chaîne **Dev → Build → Ship → Run** conteneurisée. Le vrai livrable est la chaîne DevOps, pas l'application.

## Architecture applicative (stack Docker Compose)

```
   Navigateur
       │ :8080
       ▼
 ┌──────────────────┐    /api     ┌──────────────────┐    SQL    ┌────────────────────┐
 │ frontend (nginx) │ ──────────▶ │  api (FastAPI)   │ ────────▶ │ db (PostgreSQL 16) │
 │ sert le React    │             │ uvicorn :8000    │           │ :5432 — interne    │
 │ reverse-proxy    │             │ migrations auto  │           │ volume persistant  │
 └──────────────────┘             └──────────────────┘           └────────────────────┘
          réseau privé Docker « forum-network » — la base n'est jamais exposée à l'hôte
```

**Flux nominal :**
1. Le navigateur arrive sur **nginx** (front) en `:8080`.
2. nginx **sert l'interface React** et **redirige les appels `/api`** vers l'API (reverse-proxy → évite le CORS).
3. L'**API FastAPI** applique d'abord les migrations (`alembic upgrade head`), puis `uvicorn` sert les requêtes.
4. L'API lit/écrit dans **PostgreSQL** via le réseau interne (`db:5432`) — la base n'est accessible que des services.
5. Les données sont stockées dans un **volume nommé** : elles survivent au redémarrage des conteneurs.

## Stack technique

| Couche | Choix | Justification |
|---|---|---|
| API | Python 3.12 + FastAPI 0.136 | Async léger, typage fort, doc OpenAPI (`/docs`) générée automatiquement. |
| Migrations | SQLAlchemy 2 + Alembic | Schéma de base versionné avec le code, appliqué automatiquement au démarrage. |
| Base de données | PostgreSQL 16-alpine | Relationnel adapté à la hiérarchie catégories→sujets→messages. |
| Front | React (Vite) servi par nginx | Interface légère ; nginx sert le statique + reverse-proxy `/api`. |
| Conteneurisation | Docker (Dockerfile multi-étapes) | Image finale légère et plus sûre (pas d'outils de build embarqués). |
| Orchestration locale | Docker Compose | Décrit les 3 services et leurs dépendances ; `docker compose up` lance tout. |
| CI/CD | GitHub Actions + GHCR | Intégré au dépôt, secrets natifs, publication d'image sans configuration externe. |
| Sécurité | Trivy + pip-audit + gitleaks | Scan d'image, audit des dépendances, détection de secrets — dans la CI. |

## Choix d'architecture clés

- **Trois services séparés, base non exposée.** Front, API et base communiquent sur un réseau privé ; seuls le front et l'API sont publiés (liés à `127.0.0.1`), la base reste interne.
- **Démarrage fiable et ordonné.** Un `healthcheck` sur la base + `depends_on: service_healthy` garantissent que l'API ne démarre **qu'une fois la base prête**. Les migrations s'appliquent seules au boot.
- **Secrets hors du code.** Les valeurs sensibles passent par `.env` (ignoré par Git) en local et par **GitHub Secrets** en CI ; aucun secret n'est versionné — vérifié automatiquement par **gitleaks**.
- **Publication gatée.** Le pipeline `lint → test → scan → build → push` ne publie l'image sur GHCR (taguée par SHA, donc traçable et rollback-able) **que si lint, tests et scan Trivy passent** : on ne publie que ce qu'on a contrôlé.

## Pour aller plus loin (bonus — hors périmètre évalué 2025/2026)

L'application a aussi été déployée sur **Kubernetes (minikube)** — `StatefulSet` + PVC pour la persistance Postgres, `initContainer` pour les migrations, Ingress — et instrumentée avec **Prometheus + Grafana** (scrape de `/metrics`, dashboard requêtes/s & latence). Réalisés en bonus ; le cours s'est arrêté à Docker, Compose et CI/CD.

## Limites connues & pistes

| Limite | Piste d'amélioration |
|---|---|
| Conteneurs en `root` | Ajouter un utilisateur non-root (`USER appuser`). |
| Front pas encore scanné par Trivy → non publié | Ajouter son scan, puis l'inclure dans la publication. |
| Pas de TLS (HTTP en local) | Terminaison TLS si déploiement réel. |
| Pas de cible de production réelle | Le « CD » s'arrête à la publication d'image. |

---
*Note d'architecture — soutenance S6. Cohérente avec le README et `docs/postmortem.md`.*
