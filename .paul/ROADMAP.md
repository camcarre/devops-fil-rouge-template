
# Roadmap: Forum DevOps Fil Rouge

## Overview

Le projet suit les 6 séances du fil rouge (S1→S6). Chaque séance = une phase PAUL avec un livrable précis. On part d'un forum applicatif minimal (API + PostgreSQL) et on l'industrialise progressivement : conteneurisation → docker-compose + CI → Kubernetes local → monitoring/sécurité → soutenance. La valeur monte à chaque phase ; le forum reste volontairement simple pour que l'effort porte sur la chaîne DevOps.

## Current Milestone

**v0.1 Fil Rouge (S1→S6)** (v0.1.0)
Status: In progress
Phases: 5 of 6 complete

## Phases

**Phase Numbering :** phases entières (1–6) = séances planifiées S1–S6. Phases décimales (ex. 2.1) réservées aux insertions urgentes (tag `[INSERTED]`).

| Phase | Name | Plans | Status | Completed |
|-------|------|-------|--------|-----------|
| 1 | S1 — Cadrage & Setup Git | 3 | Done | 2026-06-03 |
| 2 | S2 — Conteneurisation service + BDD | 4 | Done | 2026-06-04 |
| 3 | S3 — docker-compose + CI verte | 4 | Done | 2026-06-04 |
| 4 | S4 — Déploiement Kubernetes local | 4 | Done | 2026-06-04 |
| 5 | S5 — Monitoring + scan + post-mortem | 4 | Done | 2026-06-04 |
| 6 | S6 — Soutenance | 3 | Not started | - |

## Phase Details

### Phase 1: S1 — Cadrage & Setup Git

**Goal:** README cadrage Note 3 complet + dépôt Git initialisé + sujet forum validé par l'intervenant.
**Depends on:** Nothing (première phase)
**Research:** Unlikely (setup connu, acquis Git supposés en B3)

**Scope:**
- Former l'équipe (2–4 personnes) + canal de communication (Teams/Discord)
- Proposer le **forum** comme sujet → obtenir le go/no-go intervenant
- Créer le dépôt privé `devops-fil-rouge-<equipe>`, inviter membres + intervenant, protéger `main`
- Rédiger le README cadrage : équipe, sujet, **rôles**, **3 objectifs fil rouge**
- `.gitignore` (incluant `.env`) + `.env.example` sans valeurs réelles
- Premier commit : `chore: initial project setup and README template`
- Répondre au QCM culture (fin S1 ou <48 h)

**Plans:**
- [x] 01-01: Constituer l'équipe, répartir les 4 rôles, ouvrir le canal de communication
- [x] 01-02: Rédiger le README cadrage (sujet forum + 3 objectifs fil rouge + justifications stack 1 phrase)
- [x] 01-03: Initialiser le dépôt Git (privé, `main` protégée, `.gitignore`, `.env.example`, premier commit)

### Phase 2: S2 — Conteneurisation service + BDD

**Goal:** API forum minimale + PostgreSQL tournant en conteneurs sur un réseau Docker.
**Depends on:** Phase 1 (dépôt + stack validés)
**Research:** Likely
**Research topics:** image de base + multi-stage build, réseau Docker (DNS interne), schéma de données forum, migrations.

**Scope:**
- Modèle de données : `users`, `categories`, `topics`, `posts`
- API REST CRUD minimale (catégories / topics / posts + auth basique)
- `Dockerfile` du service (image légère, multi-stage si pertinent)
- Conteneur PostgreSQL + volume persistant
- Réseau Docker reliant `api` ↔ `db`

**Plans:**
- [x] 02-01: Schéma DB + migrations (users, categories, topics, posts)
- [x] 02-02: API CRUD catégories / topics / posts + auth simple
- [x] 02-03: Dockerfile du service + build de l'image
- [x] 02-04: Conteneur PostgreSQL + réseau Docker + smoke test api↔db

### Phase 3: S3 — docker-compose + CI verte

**Goal:** Stack lancée par `docker-compose up` + pipeline CI **vert** sur chaque PR vers `main`.
**Depends on:** Phase 2 (images + service fonctionnels)
**Research:** Likely
**Research topics:** GitHub Actions (lint/test/build), GitHub Secrets, healthchecks compose.

**Scope:**
- `docker-compose.yml` : services `api` + `db`, réseau, volumes, healthchecks, variables via `.env`
- Pipeline GitHub Actions : **lint + tests + build image**, déclenché sur push/PR vers `main`
- Secrets injectés via **GitHub Secrets** (jamais en clair)
- Badge CI dans le README

**Plans:**
- [x] 03-01: `docker-compose.yml` (api + db, env, volumes, healthchecks)
- [x] 03-02: Tests automatisés (unit + smoke API)
- [x] 03-03: Workflow `.github/workflows/ci.yml` (lint + test + build) vert
- [x] 03-04: Configurer GitHub Secrets + mettre `.env.example` à jour

### Phase 4: S4 — Déploiement Kubernetes local

**Goal:** Forum déployé et accessible sur un cluster Kubernetes local (kind / minikube).
**Depends on:** Phase 3 (image issue de la CI + compose de référence)
**Research:** Likely
**Research topics:** kind vs minikube, Deployment/Service/Ingress, ConfigMap/Secret, PVC pour PostgreSQL.

**Scope:**
- Manifests K8s `api` : Deployment, Service, ConfigMap, Secret
- Manifests K8s `db` : Deployment/StatefulSet + PVC (persistance)
- Ingress ou port-forward pour l'accès local
- Doc de déploiement (Lead Ops)

**Plans:**
- [x] 04-01: Cluster local (kind/minikube) + namespace dédié
- [x] 04-02: Manifests `api` (Deployment + Service + ConfigMap + Secret)
- [x] 04-03: Manifests `db` (StatefulSet/Deployment + PVC)
- [x] 04-04: Ingress / accès local + doc de déploiement

### Phase 5: S5 — Monitoring + scan + post-mortem

**Goal:** Observabilité (métriques + dashboards), scan de sécurité, post-mortem rédigé.
**Depends on:** Phase 4 (application déployée à observer)
**Research:** Likely
**Research topics:** exposition de métriques applicatives, scrape Prometheus, dashboards Grafana, scan image Trivy.

**Scope:**
- Endpoint métriques (`/metrics`) + Prometheus
- Dashboards Grafana (santé service, DB)
- Scan sécurité image (Trivy) + audit dépendances, intégré à la CI si possible
- Post-mortem : incidents rencontrés, choix, limites

**Plans:**
- [x] 05-01: Exposition des métriques + scrape Prometheus
- [x] 05-02: Dashboards Grafana
- [x] 05-03: Scan Trivy + audit dépendances (+ étape CI)
- [x] 05-04: Rédaction du post-mortem

### Phase 6: S6 — Soutenance

**Goal:** Démo de bout en bout + documentation finale + rétrospective.
**Depends on:** Phase 5
**Research:** Unlikely (consolidation)

**Scope:**
- Démo reproductible (docker-compose + Kubernetes)
- Doc finale (README à jour, note d'architecture, post-mortem)
- Support de soutenance + répartition de la prise de parole

**Plans:**
- [ ] 06-01: Répétition de la démo bout-en-bout
- [ ] 06-02: Doc finale + note d'architecture consolidée
- [ ] 06-03: Slides de soutenance + rétrospective équipe

---
*Roadmap created: 2026-06-03*
*Last updated: 2026-06-03*
