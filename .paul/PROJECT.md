# Forum DevOps Fil Rouge

## What This Is

Application web de **forum de discussion** (catégories → sujets → messages), volontairement minimale côté fonctionnel. Le vrai livrable du projet n'est pas le forum lui-même mais la **chaîne DevOps complète** construite autour : conteneurisation (Docker), orchestration (docker-compose puis Kubernetes local), CI/CD (GitHub Actions), monitoring et scan de sécurité. Le forum fournit une API + base de données persistante crédibles à industrialiser, conformément à l'esprit du module (« le cœur du module est DevOps, pas le framework front »).

## Core Value

Démontrer une maîtrise DevOps de bout en bout — du code conteneurisé au déploiement Kubernetes monitoré — sur une application forum simple mais réelle, **reproductible en une commande** (`docker-compose up`).

## Current State

| Attribute | Value |
|-----------|-------|
| Type | Application (web, API + DB) |
| Version | 0.0.0 |
| Status | Initializing (S1 — cadrage) |
| Last Updated | 2026-06-03 |

## Requirements

### Core Features (forum applicatif — volontairement minimal)

- **Catégories** : lister les catégories de discussion
- **Sujets (topics)** : créer et lister des sujets dans une catégorie
- **Messages (posts)** : poster et lister des messages dans un sujet
- **Comptes** : inscription + connexion simples (session ou JWT basique, **sans OAuth**)
- **API REST + persistance PostgreSQL**

### Validated (Shipped)

None yet.

### Active (In Progress)

- [ ] **S1** — README cadrage (Note 3) : équipe, sujet, rôles, 3 objectifs fil rouge

### Planned (Next)

- **S2** — Service + BDD conteneurisés, réseau Docker
- **S3** — docker-compose.yml + pipeline CI vert
- **S4** — Déploiement Kubernetes local
- **S5** — Monitoring + scan sécurité + post-mortem
- **S6** — Soutenance

### Out of Scope (rester dans les clous du cadrage)

- **Temps réel** (websockets, live updates) — *« temps réel lourd » à éviter*
- **OAuth / SSO / auth avancée** — *« authentification OAuth avancée » à éviter*
- **Microservices** — architecture monolithique simple (1 service + 1 DB)
- **Front élaboré / SPA lourde** — hors focus : le cœur est DevOps, pas le framework front
- **Modération avancée, votes, recherche full-text, notifications** — non essentiels au fil rouge

## Target Users

**Primary :** l'équipe projet (B3) + l'intervenant évaluateur — le « produit » sert l'évaluation DevOps.

**Secondary (fiction utile) :** utilisateurs d'un forum (lecteurs / posteurs) — cadre le périmètre minimal des features.

## Context

**Business Context :** projet pédagogique fil rouge sur 6 séances (S1→S6). Évaluation Note 3 dès S1 (README cadrage + QCM culture <48h + participation cas/jeu de rôle). Le sujet est proposé par le groupe et validé go/no-go par l'intervenant (~2 min/groupe).

**Technical Context :** stack minimal imposé par l'esprit du module. Persistance obligatoire (DB). Aucun secret dans Git. Dépôt privé `devops-fil-rouge-<equipe>`, branche `main` protégée, merge via Pull Request relue par au moins un autre membre.

## Constraints

### Technical Constraints

- Stack minimal, **monolithe** (1 service applicatif + 1 DB) — pas de microservices
- **Persistance obligatoire** (PostgreSQL conteneurisé)
- **Aucun secret versionné** : `.env` dans `.gitignore`, `.env.example` sans valeurs réelles, secrets CI via GitHub Secrets (S3)
- Cible de déploiement : **Kubernetes local** (kind ou minikube) en S4

### Business Constraints

- Calendrier figé : 6 séances S1→S6, un livrable attendu par séance
- Note 3 livrée dès S1 (README cadrage + QCM <48h + participation)
- Choix de stack/architecture **justifiés en une phrase** dans le README (zone d'effort étudiant)

### Compliance Constraints

- Pas de secret en clair (règle absolue du guide Git) — un secret commité = compromis → le révoquer + nettoyer l'historique

## Key Decisions

| Decision | Rationale | Date | Status |
|----------|-----------|------|--------|
| Forum comme sujet applicatif | API + DB simple, dans l'esprit « mini-blog/notes », persistance claire | 2026-06-03 | Proposé (valider intervenant S1) |
| Monolithe + PostgreSQL | Reste minimal, évite les microservices déconseillés | 2026-06-03 | Proposé |
| Pas de temps réel ni d'OAuth | Respecte les « à éviter » du cadrage | 2026-06-03 | Active |
| Stack backend à confirmer S1 | Node/Express ou Python/FastAPI — voir STACK.md | 2026-06-03 | Ouvert |

## Success Metrics (jalons du cadrage)

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| S1 — README cadrage Note 3 | équipe + sujet + rôles + 3 objectifs | - | Active |
| S2 — Service + BDD conteneurisés | réseau Docker fonctionnel | - | Not started |
| S3 — docker-compose + CI verte | pipeline vert sur chaque PR | - | Not started |
| S4 — Déploiement K8s local | app accessible sur cluster local | - | Not started |
| S5 — Monitoring + scan + post-mortem | dashboards + scan + doc | - | Not started |
| S6 — Soutenance | démo bout-en-bout + doc finale | - | Not started |

## Tech Stack / Tools (proposé — voir STACK.md, à valider S1)

| Layer | Technology | Notes |
|-------|------------|-------|
| Application | Node.js + Express *(ou Python + FastAPI)* | Stack minimal, à confirmer par le groupe |
| Database | PostgreSQL | Persistance, conteneurisable |
| Conteneurisation | Docker + docker-compose | S2–S3 |
| Orchestration | Kubernetes local (kind / minikube) | S4 |
| CI/CD | GitHub Actions | S3, secrets via GitHub Secrets |
| Monitoring | Prometheus + Grafana | S5 |
| Sécurité | Trivy (scan image) + audit dépendances | S5 |

## Links

| Resource | URL |
|----------|-----|
| Repository | `devops-fil-rouge-<equipe>` (privé — à créer S1) |
| Production | N/A (déploiement K8s local uniquement) |
| Documentation | `docs/architecture.md`, `README.md` |

---
*PROJECT.md — Updated when requirements or context change*
*Last updated: 2026-06-03*
