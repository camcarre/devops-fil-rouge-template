# Spec — Front-end Forum (style ChatGPT, intégré DevOps)

**Date :** 2026-06-04
**Auteur :** Baptiste Baudry (Lead Ops)
**Statut :** Validé (design approuvé) — prêt pour plan d'implémentation

## Contexte & objectif

Le projet `devops-fil-rouge` est un backend pur (API FastAPI + PostgreSQL) ; le front
était volontairement hors scope. On ajoute désormais un **front web** qui :

1. consomme l'API forum existante (catégories → sujets → messages, auth JWT),
2. adopte un style visuel « ChatGPT » (monochrome, minimal, system-sans),
3. **s'intègre à la chaîne DevOps** : conteneurisé, dans `docker-compose`, déployé sur
   le cluster Kubernetes (livrables Lead Ops).

Le front n'est pas un livrable noté du cadrage ; il est ajouté comme extension qui
**enrichit la démo DevOps** (front + api + db + monitoring sur le cluster).

## Décisions validées

| Décision | Choix | Raison |
|----------|-------|--------|
| Périmètre | Intégré DevOps (conteneurisé + K8s) | Cohérent rôle Lead Ops, valorise la démo |
| Mapping UI | Sidebar = catégories/sujets · centre = fil du sujet · input = poster | Transposition fidèle du layout ChatGPT au forum |
| Stack | Vite + React + TypeScript + Tailwind v4 + shadcn | Build statique léger, idéal à conteneuriser |
| Service runtime | nginx (statique + reverse-proxy `/api`) | Image légère, **évite CORS** (même origine) |

## Architecture

```
   Ingress / port-forward
     ├── /            → frontend (nginx : fichiers statiques React)
     └── /api/*       → api (FastAPI)   ← proxy nginx, réécrit /api/ → /
                          └── db (PostgreSQL, StatefulSet + PVC)
```

- **Monorepo** : nouveau dossier `frontend/` à la racine, à côté de `src/` (backend).
- Le front est **stateless** : servi en statique, tout l'état vit dans l'API/DB.
- **Pas de CORS** : nginx sert le front et proxy `/api/*` vers le service `api` →
  front et API sur la même origine. Aucune modification du backend nécessaire.

### Boundary
- Le front ne parle JAMAIS à la DB directement — uniquement via l'API.
- Aucun secret dans le front (le JWT est obtenu au login et gardé côté client).

## Écrans & composants

| Écran | Rôle | Composants shadcn |
|-------|------|-------------------|
| Shell (layout) | Sidebar gauche + zone centrale (2 colonnes) | `sidebar`, `scroll-area`, `button`, `separator` |
| Sidebar | Liste catégories → sujets, bouton « + Sujet », footer compte | `button`, `collapsible` |
| Auth | Connexion / inscription | `card`, `tabs`, `input`, `label`, `button` |
| Fil d'un sujet | Messages du sujet + champ « Écrire un message » | `card`, `textarea`, `avatar`, `button` |
| Empty state | « Where should I begin? » centré, sans déco | (texte pur) |

### Style (design tokens)
- Tokens injectés dans Tailwind v4 via `@theme` : `--color-ink-black #0d0d0d`,
  `--color-paper #f9f9f9`, `--color-snow #ffffff`, `--color-smoke #5d5d5d`,
  `--color-ash #8f8f8f`, `--color-fog #ececec`.
- Radius 10px (inputs/boutons/nav), 28px (grands conteneurs). System-sans partout.
- **Discipline** : zéro couleur d'accent, zéro ombre (sauf bordure 1px `#ececec` sur
  l'input), zéro image. Poids de police ≤ 600. Séparation sidebar/centre par le
  contraste Paper→Snow, pas de bordure.
- Le thème par défaut de shadcn est **écrasé** pour respecter le monochrome.

## Intégration API & auth

- Module `frontend/src/lib/api.ts` : wrapper `fetch` typé vers `/api/...`.
- Endpoints consommés : `POST /api/auth/register`, `POST /api/auth/login`,
  `GET/POST /api/categories/`, `GET/POST /api/categories/{id}/topics`,
  `GET/POST /api/topics/{id}/posts`.
- **Auth JWT** : token stocké (localStorage), envoyé en `Authorization: Bearer`.
- **Quirk login encapsulé** : `/auth/login` attend l'**email** dans le champ `username`
  + `application/x-www-form-urlencoded`. Le wrapper le gère de façon transparente.

## Conteneurisation & déploiement (Lead Ops)

- `frontend/Dockerfile` multi-stage : `node` (build Vite) → `nginx:alpine` (statique).
- `frontend/nginx.conf` : sert `/` (SPA fallback `index.html`) + `location /api/ { proxy_pass http://api:8000/; }`.
- `docker-compose.yml` : service `frontend` (build `./frontend`, dépend de `api`, port 8080).
- K8s : `k8s/50-frontend-deployment.yaml`, `k8s/51-frontend-service.yaml`, route ingress
  `/` vers le front (l'API passe derrière `/api`).

## Plans d'implémentation (séquence)

1. **F1** — Scaffold Vite+React+TS+Tailwind v4+shadcn + tokens du design (thème monochrome).
2. **F2** — Shell : layout 2 colonnes, sidebar catégories/sujets, empty state.
3. **F3** — Auth : écrans login/register branchés sur l'API (gestion du quirk + JWT).
4. **F4** — Fil d'un sujet : afficher les messages + poster un message.
5. **F5** — Conteneurisation : Dockerfile nginx + reverse-proxy + service compose.
6. **F6** — Déploiement K8s : manifests frontend + route ingress, vérifié sur le cluster.

## Tests
- `frontend/src/lib/api.test.ts` : test du wrapper API (mock `fetch`, vérifie le quirk login).
- Un test de rendu du Shell (la sidebar liste bien les catégories mockées).
- Volontairement léger — le focus du projet reste DevOps, pas la couverture front.

## Hors scope
- Pas de SSR, pas de state management lourd (Redux…), pas de temps réel, pas de
  fonctionnalités forum avancées (votes, recherche full-text, modération).
- Pas de design responsive avancé au-delà d'un layout desktop propre + dégradé mobile simple.
