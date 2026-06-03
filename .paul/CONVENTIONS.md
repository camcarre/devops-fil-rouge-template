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

| Plan | Branche |
|------|---------|
| 01-01 | `feature/01-01-team-setup` |
| 01-02 | `feature/01-02-readme-cadrage` |
| 01-03 | `feature/01-03-git-setup` |
| 02-01 | `feature/02-01-db-schema` |
| 02-02 | `feature/02-02-api-crud` |
| 02-03 | `feature/02-03-dockerfile-api` |
| 02-04 | `feature/02-04-postgres-network` |
| 03-01 | `feature/03-01-docker-compose` |
| 03-02 | `feature/03-02-tests` |
| 03-03 | `feature/03-03-ci-workflow` |
| 03-04 | `feature/03-04-ci-secrets` |
| 04-01 | `feature/04-01-k8s-cluster` |
| 04-02 | `feature/04-02-k8s-api` |
| 04-03 | `feature/04-03-k8s-db` |
| 04-04 | `feature/04-04-k8s-ingress` |
| 05-01 | `feature/05-01-metrics-prometheus` |
| 05-02 | `feature/05-02-grafana-dashboards` |
| 05-03 | `feature/05-03-security-scan` |
| 05-04 | `feature/05-04-post-mortem` |
| 06-01 | `feature/06-01-demo-rehearsal` |
| 06-02 | `feature/06-02-final-docs` |
| 06-03 | `feature/06-03-soutenance-slides` |

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

| Rôle | Responsabilités | Titulaire |
|------|-----------------|-----------|
| Lead Dev | Code applicatif, Dockerfile du service | _à remplir_ |
| Lead Ops | Compose, K8s, monitoring, doc déploiement | _à remplir_ |
| Lead Qualité / CI | Pipeline, tests, revue sécurité de base | _à remplir_ |
| Lead Produit / Doc | README, note d'archi, post-mortem | _à remplir_ |

> Un membre peut cumuler 2 rôles dans un petit groupe — documenter qui fait quoi.

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
*Last updated: 2026-06-03*
