# STACK — Forum DevOps Fil Rouge

> Libs + outils, avec justification (zone d'effort étudiant : chaque choix justifié en une phrase). **Proposé — à valider en S1.** Reuse > Invent : pas de nouvelle dépendance sans l'ajouter ici.

## Statut

Stack **proposée**, non figée. Le groupe propose, l'intervenant valide (S1). Toute version est indicative tant que la décision n'est pas prise.

## Application

| Élément | Choix proposé | Alternative | Justification (1 phrase) |
|---------|---------------|-------------|--------------------------|
| Langage / framework | Node.js 20 LTS + Express | Python 3.12 + FastAPI | Stack minimale et largement connue, suffisante pour une API CRUD forum. |
| Base de données | PostgreSQL 16 | — | Relationnel adapté au modèle catégories→topics→posts, persistance robuste et conteneurisable. |
| Accès DB / migrations | Outil natif du framework (ex. node-pg-migrate / Alembic) | — | Migrations versionnées = schéma reproductible en CI et K8s. |
| Auth | Session ou JWT basique | — | Authentification simple, sans OAuth (déconseillé par le cadrage). |
| Front | Templates server-side **ou** petit front statique | — | Le front n'est pas le focus du module ; minimal volontairement. |

## DevOps / Infra

| Élément | Choix | Séance | Justification (1 phrase) |
|---------|-------|--------|--------------------------|
| Conteneurisation | Docker | S2 | Standard de packaging reproductible du service et de la DB. |
| Orchestration locale | docker-compose | S3 | Lance toute la stack en une commande pour le dev et la CI. |
| Orchestration cible | Kubernetes local (kind ou minikube) | S4 | Cible d'industrialisation imposée par le module. |
| CI/CD | GitHub Actions | S3 | Intégré au dépôt, gère lint/test/build et les secrets via GitHub Secrets. |
| Monitoring | Prometheus + Grafana | S5 | Scrape de `/metrics` + dashboards = observabilité standard. |
| Sécurité | Trivy + audit dépendances | S5 | Scan d'image et de dépendances pour la revue sécurité de base. |

## Services externes

Aucun service externe payant ou tiers requis. Tout tourne en local (Docker/K8s). Aucune clé d'API tierce nécessaire au cœur du projet.

## Gestion des secrets

- `.env` (jamais commité, listé dans `.gitignore`)
- `.env.example` (noms de variables, sans valeurs) — versionné
- CI : **GitHub Secrets**
- K8s : **Secret** + ConfigMap

Variables attendues (cf. `.env.example`) : `DATABASE_URL`, `API_KEY`, `PORT`.

---
*Last updated: 2026-06-03*
