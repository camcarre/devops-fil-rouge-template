# CONVENTIONS — Forum DevOps Fil Rouge

> Naming, Git, commits, structure, tests. Reprend le guide Git du module (`guide-git-travail-groupe`). Source de vérité cross-phase.

## Workflow Git (petit groupe)

```
main (protégée) ← merge via Pull Request après revue
    ↑
feature/xxx (une branche par tâche ou par personne)
```

Cycle de travail :
1. `git pull origin main` avant de commencer
2. `git checkout -b feature/<tache>` (ex. `feature/dockerfile-api`)
3. Commits **petits et explicites**
4. `git push -u origin feature/<tache>`
5. **Pull Request** + relecture par **au moins un autre membre**
6. Merge → **supprimer la branche** feature

Règles dépôt :
- Dépôt **privé** nommé `devops-fil-rouge-<equipe>`
- Branche de base = **`master`** (défaut du repo ; le guide cite `main` — même rôle). **Protégée** : merge via PR uniquement
- Membres + intervenant invités

## Branches feature (créées, poussées sur origin)

Une branche par tâche de la roadmap, préfixe `feature/<plan>-<slug>`, toutes parties de `master`.

> ⚠️ Branches créées **d'avance** : avant de travailler sur l'une, la remettre à jour
> (`git checkout feature/xxx` → `git rebase master` après `git pull origin master`),
> sinon elle diverge de `master`. Méthode agile stricte = brancher à la demande.

Chaque branche a un **rôle propriétaire** (responsable de l'avancement + ouverture de la PR). La revue est faite par **un autre membre** (cf. workflow Git).

| Plan | Branche | Rôle propriétaire | Titulaire |
|------|---------|-------------------|-----------|
| 01-01 | `feature/01-01-team-setup` | Responsable équipe | Alvin Savi |
| 01-02 | `feature/01-02-readme-cadrage` | Lead Produit / Doc | Cléo Doroo |
| 01-03 | `feature/01-03-git-setup` | Responsable équipe | Alvin Savi |
| 02-01 | `feature/02-01-db-schema` | Lead Dev | Théo Delporte |
| 02-02 | `feature/02-02-api-crud` | Lead Dev | Théo Delporte |
| 02-03 | `feature/02-03-dockerfile-api` | Lead Dev | Théo Delporte |
| 02-04 | `feature/02-04-postgres-network` | Lead Ops | Baptiste Baudry |
| 03-01 | `feature/03-01-docker-compose` | Lead Ops | Baptiste Baudry |
| 03-02 | `feature/03-02-tests` | Lead Qualité / CI | Camille Douaud |
| 03-03 | `feature/03-03-ci-workflow` | Lead Qualité / CI | Camille Douaud |
| 03-04 | `feature/03-04-ci-secrets` | Lead Qualité / CI | Camille Douaud |
| 04-01 | `feature/04-01-k8s-cluster` | Lead Ops | Baptiste Baudry |
| 04-02 | `feature/04-02-k8s-api` | Lead Ops | Baptiste Baudry |
| 04-03 | `feature/04-03-k8s-db` | Lead Ops | Baptiste Baudry |
| 04-04 | `feature/04-04-k8s-ingress` | Lead Ops | Baptiste Baudry |
| 05-01 | `feature/05-01-metrics-prometheus` | Lead Ops (+ Lead Dev pour `/metrics`) | Baptiste Baudry |
| 05-02 | `feature/05-02-grafana-dashboards` | Lead Ops | Baptiste Baudry |
| 05-03 | `feature/05-03-security-scan` | Lead Qualité / CI | Camille Douaud |
| 05-04 | `feature/05-04-post-mortem` | Lead Produit / Doc | Cléo Doroo |
| 06-01 | `feature/06-01-demo-rehearsal` | Responsable équipe | Alvin Savi |
| 06-02 | `feature/06-02-final-docs` | Lead Produit / Doc | Cléo Doroo |
| 06-03 | `feature/06-03-soutenance-slides` | Lead Produit / Doc (+ Responsable équipe) | Cléo Doroo |

## Convention de commits

| Préfixe | Usage |
|---------|-------|
| `feat:` | Nouvelle fonctionnalité |
| `fix:` | Correction de bug |
| `chore:` | Config, README, outillage |
| `docs:` | Documentation seule |
| `ci:` | Pipeline CI/CD |

Exemples : `feat: add Dockerfile for API service` · `ci: add lint and test workflow on push to main` · `chore: initial project setup and README template`

## Secrets — règle absolue

**Interdit dans Git :** mots de passe DB, tokens API, clés AWS/GitHub, fichiers `.env` avec secrets.

**À faire :**
- `.env.example` avec noms de variables, **sans valeurs réelles**
- `.env` listé dans `.gitignore`
- Secrets injectés en CI via GitHub Secrets (S3)
- `git diff` **avant chaque commit** pour vérifier l'absence de secret
- Si un secret est commité → le considérer **compromis**, le révoquer, nettoyer l'historique (intervenant si besoin)

## Checklist avant chaque séance

- [ ] `git pull` sur `main`
- [ ] Aucun conflit non résolu
- [ ] Aucun secret dans le diff (`git diff` avant commit)
- [ ] README à jour si le périmètre du groupe a changé

## Fichiers à versionner dès S1

```
.
├── README.md          # Gabarit cadrage (Note 3)
├── .gitignore
├── .env.example
└── (code applicatif à venir)
```

## Rôles équipe

| Rôle                    | Responsabilités                                   | Titulaire           |
|-------------------------|---------------------------------------------------|---------------------|
| **Lead Dev**            | Code applicatif, Dockerfile du service            | Théo Delporte       |
| **Lead Ops**            | Compose,     monitoring, documentation déploiement| Baptiste Baudry     |
| **Lead Qualité / CI**   | Pipeline, tests, revue sécurité de base           | Camille Douaud      |
| **Lead Produit / Doc**  | README, note d'architecture, post-mortem          | Cléo Doroo          |
| **Responsable équipe**  | Animation/coordination                            | Alvin Savi          |

**Canal de communication :** Teams / Discord — à préciser

> Un membre peut cumuler 2 rôles dans un petit groupe — documenter qui fait quoi.

### Détail des responsabilités par rôle (qui fait quoi)

**Lead Dev — Théo Delporte**
- Modèle de données + migrations (`02-01`)
- API REST forum : auth JWT + CRUD catégories/topics/posts (`02-02`)
- Dockerfile du service applicatif, image légère multi-stage (`02-03`)
- Endpoint applicatif `/metrics` exposant les métriques (appui sur `05-01`)

**Lead Ops — Baptiste Baudry**
- Conteneur PostgreSQL + volume persistant + réseau Docker `api`↔`db` (`02-04`)
- `docker-compose.yml` : services, réseau, volumes, healthchecks (`03-01`)
- Manifests Kubernetes : cluster local, `api`, `db`+PVC, Ingress/accès (`04-01`→`04-04`)
- Monitoring : scrape Prometheus + dashboards Grafana (`05-01`, `05-02`)
- Documentation de déploiement

**Lead Qualité / CI — Camille Douaud**
- Tests automatisés unitaires + smoke API (`03-02`)
- Pipeline GitHub Actions lint+test+build, vert sur PR vers base (`03-03`)
- Gestion des secrets CI via GitHub Secrets + maj `.env.example` (`03-04`)
- Revue sécurité : scan image Trivy + audit dépendances (`05-03`)

**Lead Produit / Doc — Cléo Doroo**
- README cadrage Note 3 : sujet, rôles, 3 objectifs (`01-02`)
- Post-mortem : incidents, choix, limites (`05-04`)
- Doc finale + note d'architecture consolidée (`06-02`)
- Contribution aux slides de soutenance (`06-03`)

**Responsable équipe — Alvin Savi**
- Constitution équipe, répartition des rôles, canal de communication (`01-01`)
- Dépôt Git privé, protection `master`, invitations, `.gitignore`/`.env.example`, premier commit (`01-03`)
- Animation/coordination, suivi de l'avancement cross-phase
- Répétition de la démo bout-en-bout (`06-01`) + slides/prise de parole (`06-03`)

## Structure de projet (cible, indicative)

```
.
├── README.md
├── .gitignore
├── .env.example
├── docs/architecture.md
├── src/                  # code applicatif (S2)
├── Dockerfile            # (S2)
├── docker-compose.yml    # (S3)
├── .github/workflows/    # CI (S3)
└── k8s/                  # manifests Kubernetes (S4)
```

## Tests

- Tests automatisés requis dès S3 (intégrés à la CI) : unitaires + smoke test API.
- Un test qui passe ≠ feature OK — vérifier le comportement réel (API/UI) si pertinent.

---
*Last updated: 2026-06-04*
