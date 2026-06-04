# Forum DevOps Fil Rouge

[![CI](https://github.com/camcarre/devops-fil-rouge-template/actions/workflows/ci.yml/badge.svg)](https://github.com/camcarre/devops-fil-rouge-template/actions/workflows/ci.yml)

**Équipe :** Théo Delporte, [Prénom Nom], [Prénom Nom], [Prénom Nom]
**Groupe / promo :** B3 — [Promo — à remplir]
**Dépôt :** https://github.com/[organisation]/devops-fil-rouge-[equipe]

---

## Description du sujet

Application web de forum de discussion organisée en catégories, sujets et messages. Les utilisateurs peuvent s'inscrire, se connecter, créer des sujets dans une catégorie et y poster des messages. L'application expose une API REST avec persistance PostgreSQL. Le vrai livrable du projet est la chaîne DevOps construite autour : conteneurisation, orchestration, CI/CD, monitoring et sécurité.

---

## Stack technique prévu

| Composant | Choix | Justification (1 phrase) |
| --------- | ----- | -------------------------- |
| Backend / API | Python 3.12 + FastAPI | Framework async léger adapté à une API CRUD, typage fort et documentation OpenAPI automatique. |
| Base de données | PostgreSQL 16 | Modèle relationnel adapté à la hiérarchie catégories → topics → posts, conteneurisable et robuste. |
| Front (optionnel) | Templates server-side (Jinja2) | Le front n'est pas le focus du module ; rendu serveur minimal sans dépendance JS lourde. |
| Orchestration cible | Docker Compose (S3) puis Kubernetes local (S4) | Progression naturelle : stack locale d'abord, industrialisation K8s ensuite. |

---

## Rôles dans l'équipe

| Membre | Rôle | Responsabilité principale |
| ------ | ---- | ------------------------- |
| Théo Delporte | Lead Dev | Code applicatif, modèles SQLAlchemy, API FastAPI, Dockerfile |
| [Prénom Nom] | Lead Ops | docker-compose, manifests Kubernetes, monitoring, doc déploiement |
| [Prénom Nom] | Lead Qualité / CI | Pipeline GitHub Actions, tests automatisés, scan sécurité |
| Cléo Deroo | Lead Produit / Doc | README, note d'architecture, post-mortem |

Canal de communication : [Teams / Discord — à remplir]

---

## Objectifs du fil rouge

1. Avoir l'API forum conteneurisée avec healthcheck fonctionnel et accessible via `docker-compose up` d'ici S3.
2. Mettre en place un pipeline CI GitHub Actions qui build, teste et valide l'image sur chaque PR vers master d'ici S3.
3. Déployer l'application sur un cluster Kubernetes local (kind) avec persistance PostgreSQL via PVC d'ici S4.

---

## Jalons — état d'avancement

| Séance | Livrable | Statut |
| ------ | -------- | ------ |
| S1 | README cadrage | ☐ |
| S2 | Dockerfile(s) + DB en container | ☐ |
| S3 | docker-compose + CI vert | ☐ |
| S4 | Manifests K8s appliqués | ☐ |
| S5 | Monitoring + post-mortem | ☐ |
| S6 | Soutenance prête | ☐ |

---

## Démarrage local (à compléter au fil des séances)

```bash
# À documenter progressivement — pas besoin de tout remplir en S1
git clone https://github.com/[organisation]/devops-fil-rouge-[equipe]
cd devops-fil-rouge-[equipe]
cp .env.example .env
# Remplir les valeurs dans .env
```

---

## Communication d'équipe

Canal utilisé : [Teams / Discord — à remplir]

---

## Participation S1

Jeu de rôle déploiement : leçon retenue — un secret commité dans Git est considéré compromis et doit être révoqué immédiatement, même si l'historique est nettoyé ensuite. La règle `.env` dans `.gitignore` dès le premier commit évite ce risque.
