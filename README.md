# Forum DevOps Fil Rouge

[![CI](https://github.com/camcarre/devops-fil-rouge-template/actions/workflows/ci.yml/badge.svg)](https://github.com/camcarre/devops-fil-rouge-template/actions/workflows/ci.yml)

**Équipe :** Alvin Savi, Théo Delporte, Baptiste Baudry, Camille, Cléo Deroo
**Groupe / promo :** Bachelor 3 — Informatique (Gestion du SI)
**Dépôt :** https://github.com/camcarre/devops-fil-rouge-template

---

## Description du sujet

Application web de forum de discussion organisée en catégories, sujets et messages. Les utilisateurs peuvent s'inscrire, se connecter, créer des sujets dans une catégorie et y poster des messages. L'application expose une API REST avec persistance PostgreSQL. Le vrai livrable du projet est la chaîne DevOps construite autour : conteneurisation, orchestration, CI/CD, monitoring et sécurité.

---

## Stack technique prévu

| Composant | Choix | Justification (1 phrase) |
| --------- | ----- | -------------------------- |
| Backend / API | Python 3.12 + FastAPI | Framework async léger adapté à une API CRUD, typage fort et documentation OpenAPI automatique. |
| Base de données | PostgreSQL 16 | Modèle relationnel adapté à la hiérarchie catégories → topics → posts, conteneurisable et robuste. |
| Front | React (Vite) servi par nginx | Interface de forum légère ; nginx sert les fichiers statiques et fait reverse-proxy `/api` (évite le CORS). |
| Orchestration cible | Docker Compose (S3) puis Kubernetes local (S4) | Progression naturelle : stack locale d'abord, industrialisation K8s ensuite. |

---

## Rôles dans l'équipe

| Membre | Rôle | Responsabilité principale |
| ------ | ---- | ------------------------- |
| Alvin Savi | Chef d'équipe | Coordination, planning, répartition des tâches |
| Théo Delporte | Lead Dev | Code applicatif, modèles SQLAlchemy, API FastAPI, Dockerfile |
| Baptiste Baudry | Lead Ops | docker-compose, déploiement, publication des images (GHCR), doc d'exploitation |
| Camille | Lead Qualité / CI | Pipeline GitHub Actions, tests automatisés, scan sécurité |
| Cléo Deroo | Lead Produit / Doc | README, note d'architecture, post-mortem |

Canal de communication : Microsoft Teams

---

## Objectifs du fil rouge

1. Avoir l'API forum conteneurisée avec healthcheck fonctionnel et accessible via `docker-compose up` d'ici S3.
2. Mettre en place un pipeline CI GitHub Actions qui build, teste et valide l'image sur chaque PR vers master d'ici S3.
3. Déployer l'application sur un cluster Kubernetes local (minikube) avec persistance PostgreSQL via PVC d'ici S4.

---

## Jalons — état d'avancement

| Séance | Livrable | Statut |
| ------ | -------- | ------ |
| S1 | README cadrage | ✅ |
| S2 | Dockerfile(s) + DB en container | ✅ |
| S3 | docker-compose + CI verte | ✅ |
| S4 | Manifests K8s appliqués | ✅ |
| S5 | Monitoring + post-mortem | ✅ |
| S6 | Soutenance prête | 🔄 En cours |

- Post-mortem : `docs/postmortem.md`
- Note d'architecture : `docs/architecture.md`

---

## Démarrage local

```bash
git clone https://github.com/camcarre/devops-fil-rouge-template
cd devops-fil-rouge-template
cp .env.example .env
# Remplir les valeurs dans .env
```

---

## Communication d'équipe

Canal utilisé : Microsoft Teams

---

## Participation S1

Jeu de rôle déploiement : leçon retenue — un secret commité dans Git est considéré compromis et doit être révoqué immédiatement, même si l'historique est nettoyé ensuite. La règle `.env` dans `.gitignore` dès le premier commit évite ce risque.

---

## Lancer la démo

### docker-compose (local, dev)
```bash
cp .env.example .env  # compléter les valeurs
docker-compose up
# API disponible sur http://localhost:8000
# Docs Swagger : http://localhost:8000/docs
```

### Kubernetes (minikube, cible S4-S5)
Voir [k8s/README.md](k8s/README.md) pour la séquence complète :
démarrage du cluster → déploiement des manifests → accès API, Prometheus et Grafana.

---

## CI/CD — publication des images

À chaque push sur `master`, le pipeline GitHub Actions (`.github/workflows/ci.yml`)
lint + teste + scanne + build, puis **publie l'image Docker de l'API sur GHCR**
(GitHub Container Registry), taguée par le **SHA du commit** pour la traçabilité et le rollback.

> Choix **GHCR** (vs Docker Hub) : intégré au dépôt et authentifié par le `GITHUB_TOKEN`
> intégré — aucun secret à créer manuellement.

La publication est **gatée** sur le lint, les tests et le scan **Trivy** de l'image API
(`ignore-unfixed` : on ne bloque que sur les failles corrigeables). **Règle : on ne publie
que ce qu'on scanne** — l'image frontend (nginx statique) n'est donc pas encore publiée,
le temps d'ajouter son scan.

Image publiée :
```
ghcr.io/camcarre/devops-fil-rouge-template-api:<sha>
```
