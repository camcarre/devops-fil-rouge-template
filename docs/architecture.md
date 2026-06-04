# Architecture — Forum DevOps Fil Rouge

> Ce document décrit l'architecture applicative et d'infrastructure du projet fil rouge DevOps.
> Source de vérité : `.paul/ARCHITECTURE.md`. Mis à jour pour la soutenance S6.

---

## Vue d'ensemble

```
  ┌──────────┐       ┌──────────────────────────────────────────────────────────┐
  │ Navigateur│       │                    minikube cluster                        │
  │          │       │                    namespace: forum                       │
  │          │       │                                                          │
  │ GET /    │       │  ┌──────────┐   ┌─────────────┐   ┌─────────────────────┐ │
  │ health   │──────▶│  │ Ingress  │──▶│ Service api │──▶│ Deployment api     │ │
  │          │       │  │(nginx,   │   │ (ClusterIP  │   │  FastAPI + uvicorn  │ │
  │          │       │  │forum.loc)│   │  8000)      │   │  + readiness/live   │ │
  └──────────┘       │  └──────────┘   └─────────────┘   │  + /health          │ │
                     │                                     │  + /metrics         │ │
                     │                                     └──────────┬──────────┘ │
                     │                                                │            │
                     │  ┌──────────┐   ┌─────────────┐                │            │
                     │  │ Grafana  │◀──│ Prometheus  │◀───────────────┘            │
                     │  │ :3000    │   │ :9090       │   scrape /metrics             │
                     │  └──────────┘   └─────────────┘                               │
                     │                                                          │
                     │  ┌──────────────┐   ┌──────────────────────────────┐       │
                     │  │ Service db   │──▶│ StatefulSet db               │       │
                     │  │ (headless,   │   │  postgres:16-alpine           │       │
                     │  │  db:5432)    │   │  + volumeClaimTemplate (1Gi)  │       │
                     │  └──────────────┘   │  = PersistentVolumeClaim     │       │
                     │                      │  attaché à /var/lib/postgres │       │
                     │                      └──────────────────────────────┘       │
                     └──────────────────────────────────────────────────────────┘
                               minikube tunnel / port-forward
```

**Flux nominal :**
1. Le navigateur (ou `curl`) envoie une requête HTTP vers `forum.local` (ou `localhost:8000` via port-forward).
2. L'Ingress nginx-route redirige vers le Service `api` (ClusterIP).
3. Le Deployment `api` (FastAPI/uivcorn) reçoit la requête. Avant le premier démarrage, un `initContainer` a appliqué les migrations Alembic sur la base.
4. L'API lit/écrit les données dans PostgreSQL via `DATABASE_URL` → service `db:5432`.
5. Le middleware Prometheus de l'API expose `/metrics` → Prometheus scrape toutes les 15 s → stocke les séries temporelles.
6. Grafana se connecte à Prometheus via sa datasource provisionnée et affiche le dashboard applicatif (requêtes/s, latence p95).

---

## Stack technique

| Couche          | Technologie               | Version       | Justification |
|-----------------|---------------------------|---------------|---------------|
| Langage / FW    | Python 3.12 + FastAPI     | 3.12 / 0.111  | Async, typage fort, OpenAPI auto-généré ; suffisant pour CRUD forum. |
| ORM / migrations| SQLAlchemy + Alembic      | 2.x / 1.15    | Schéma versionné et reproductible en CI et en K8s initContainer. |
| Base de données | PostgreSQL                | 16-alpine     | Relationnel adapté au modèle catégories→topics→posts, conteneurisable et robuste. |
| Conteneurisation| Docker                    | 24            | Standard de packaging reproductible (service API + base). |
| Orchestration locale | Kubernetes (minikube) | 1.30        | Cible d'industrialisation imposée par le module ; addons ingress + metrics-server intégrés. |
| CI/CD           | GitHub Actions            | —             | Intégré au dépôt, gère build/test et secrets via GitHub Secrets. |
| Monitoring      | Prometheus + Grafana      | 2.x / 11.x    | Scrape /metrics exposé par FastAPI, dashboards provisionnés via ConfigMap K8s. |
| Scan sécurité   | Trivy + pip-audit         | 0.53 / 0.1    | Scan d'image conteneur et audit dépendances Python dans la CI (échec sur HIGH/CRITICAL). |

---

## Chaîne DevOps — évolution par séance

### S1 — Cadrage et choix de stack
L'équipe valide le sujet forum, les rôles (Lead Dev, Lead Ops, Lead Qualité, Lead Produit) et la stack technique.
Décisions : Python + FastAPI (vs Node/Express), PostgreSQL 16, Docker, minikube (vs kind), GitHub Actions.
Règle duré : aucun secret commité. Le `.env` est créé et immédiatement ajouté au `.gitignore`.

### S2 — Conteneurisation
Premier `Dockerfile` pour l'API. Image PostgreSQL officielle récupérée. Les deux services tournent sur un réseau DockerBridge.
Apprentissage clé : un secret commité même brièvement = considéré compromis → révocation immédiate.

### S3 — Orchestration Docker Compose + CI
`docker-compose.yml` unifie le démarrage local (`up`). GitHub Actions vérifie `docker compose build` + `pytest` sur chaque PR.
CI intègre lint (`ruff`), tests, et build d'image sur la branche master.

### S4 — Kubernetes local (minikube)
Migration de Docker Compose vers des manifests Kubernetes :
- Namespace `forum`, ConfigMap, Secret (gabarit `examples/`).
- `StatefulSet` + `volumeClaimTemplate` pour PostgreSQL (PVC 1 Gi, `ReadWriteOnce`).
- `Deployment` pour l'API avec `initContainer` (Alembic migrate avant uvicorn).
- Ingress nginx-route (`forum.local`) + `minikube tunnel` sur macOS driver Docker.
Choix minikube vs kind : addons intégrés (ingress-nginx, metrics-server) accélèrent le setup monitoring.

### S5 — Monitoring + Sécurité
Exposition de `/metrics` via `prometheus-client` dans FastAPI. Prometheus scrape la ConfigMap.
Grafana provisionné avec datasource + dashboard applicatif (requêtes/s, latence p95).
CI enrichie : Trivy scanne l'image construite (échec sur HIGH/CRITICAL) + `pip-audit` audite les dépendances Python.

### S6 — Soutenance
Dossier documentaire finalisé (architecture.md, README, k8s/README). Démonstration live du cluster minikube avec portail API, Prometheus et Grafana.

---

## Choix d'architecture clés

### Monolithe (1 service + 1 base)
Le projet est un fil rouge DevOps, pas un exercice de conception microservices. Un seul service applicatif (FastAPI) et une seule base (PostgreSQL) suffisent pour illustrer la chaîne CI/CD, l'orchestration, le monitoring et la sécurité. Toute tentation de découpage (auth service, notification service…) est explicitement hors scope.

### minikube vs kind
minikube est retenu pour ses addons intégrés (`ingress`, `metrics-server`) qui activent le monitoring Prometheus en une commande sans configuration manuelle supplémentaire. kind serait plus léger mais demanderait une configuration ingress et un exporter Node exporter additionnel. Le driver Docker sur macOS fonctionne correctement avec `minikube tunnel`.

### StatefulSet + PVC pour la base de données
PostgreSQL est déployé en `StatefulSet` (et non `Deployment`) car il possède une identité stable et un stockage persistant. Le `volumeClaimTemplate` garantit que le PVC de 1 Gi reste attaché au même pod entre les redéploiements → la donnée survit au restart de l'application. Le path `PGDATA=/var/lib/postgresql/data/pgdata` avec `subPath` évite l'erreur "data directory not empty" au premier démarrage.

### initContainer pour les migrations
Avant que le conteneur principal uvicorn ne démarre, un `initContainer` exécute `alembic upgrade head`. Ce pattern sépare proprement le provisionnement du schéma (one-shot) du service des requêtes. L'image sama est utilisée (pas d'image de migration dédiée) pour éviter de maintenir une image supplémentaire.

### bcrypt direct (sans passlib en 1.7.x)
`passlib` 1.7.4 est incompatible avec `bcrypt` 5.x (erreur `bcrypt password hashing is not supported`). Solution : hashing direct via `bccrypt.hashpw` / `bcrypt.checkpw` sans passlib. Simple, sans dépendance supplémentaire.

### Secret K8s gitignoré + gabarit `examples/`
Le manifest `k8s/02-secret.yaml` contient les valeurs réelles (passwords) et n'est **jamais** commité. Le gabarit `k8s/examples/secret.example.yaml` (valeurs vides) est versionné et sert de référence. L'équipe copie le gabarit, le remplit et l'applique localement. Les valeurs de secret sont aussi dans GitHub Secrets pour la CI.

---

## Limites connues

| Limite | Détail | Impact |
|--------|--------|--------|
| Pas de TLS | L'Ingress est HTTP uniquement ; pas de CertManager ni Let's Encrypt. | Navigateur affiche un avertissement "non sécurisé". Hors scope module (cluster local uniquement). |
| Cluster local uniquement | minikube + Docker Desktop. Aucune configuration cloud (GKE, EKS, AKS) n'estprovisionnée. | Pas de haute disponibilité ni de persistence cross-environnement. |
| Pas de HPA ni auto-scaling | Le Deployment `api` a un nombre fixe de replicas (1). | Le service ne absorbe pas de pic de charge spontané. |
| Grafana sans authentification | Aucune authentification par défaut (admin/admin). | Risque d'accès non autorisé sur un environnement partagé. Solution : limiter l'accès réseau au cluster. |
| Monitoring applicatif uniquement | Pas de métriques DBDedans (requêtes PostgreSQL, connections actives). | Visibilité limitée sur la santé de la base. |
| Image locale via `minikube image load` | Pas de registry Docker. L'image doit être rechargée à chaque création de cluster. | Pas de partage d'image entre machines. |

---

*Document mis à jour pour la soutenance S6. Cohérent avec `.paul/ARCHITECTURE.md`, `.paul/STACK.md` et `docs/postmortem.md`.*
