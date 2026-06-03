# ARCHITECTURE — Forum DevOps Fil Rouge

> Source de vérité cross-phase. Reuse > Invent : vérifier ce doc avant d'introduire une couche, un service ou un boundary.

## Principe directeur

**Monolithe simple, industrialisé progressivement.** Le cœur du projet est la chaîne DevOps, pas la complexité applicative. Une seule application (API REST) + une seule base de données. Toute tentation de microservices, temps réel ou auth avancée est explicitement hors scope (voir PROJECT.md).

## Vue d'ensemble (cible finale, S4)

```
                 Ingress / port-forward (local)
                          │
                  ┌───────▼────────┐
                  │   api (forum)  │  Deployment + Service
                  │  REST + auth   │
                  └───────┬────────┘
                          │  réseau interne
                  ┌───────▼────────┐
                  │  PostgreSQL    │  StatefulSet/Deployment + PVC
                  │  (persistance) │
                  └────────────────┘
        Observabilité : /metrics → Prometheus → Grafana (S5)
```

## Couches (layering)

| Couche | Responsabilité | Règle dure |
|--------|----------------|------------|
| API / routes | Entrées HTTP, validation aux frontières | Pas de SQL direct ici |
| Service / domaine | Logique forum (catégories, topics, posts) | Pas de dépendance au framework HTTP |
| Data access | Requêtes DB, migrations | Seule couche qui parle à PostgreSQL |
| Infra (Docker/K8s/CI) | Build, déploiement, observabilité | Aucune logique métier |

## Boundaries durs

- **1 service applicatif, 1 base** — pas de découpage en microservices.
- **Aucun secret dans le code ni dans Git** — config par variables d'environnement (ConfigMap/Secret en K8s, GitHub Secrets en CI).
- **La persistance vit dans la DB** (volume Docker en S2-S3, PVC en S4) — jamais dans le conteneur applicatif (stateless).
- **L'app expose son état** : healthcheck + `/metrics` pour compose, K8s et Prometheus.

## Évolution de l'architecture par séance (ADRs implicites)

| Séance | Décision d'architecture | Raison |
|--------|------------------------|--------|
| S2 | Conteneuriser api + db séparément sur un réseau Docker | Isoler service et données, base de la reproductibilité |
| S3 | Orchestrer via `docker-compose` + CI build/test | Un point d'entrée unique + non-régression automatisée |
| S4 | Passer à Kubernetes local (Deployment/Service/PVC) | Cible d'industrialisation du module |
| S5 | Ajouter métriques + monitoring + scan | Observabilité et sécurité = exigences DevOps |

## Décisions ouvertes (à trancher en S1/S2)

- Framework backend (Node/Express vs Python/FastAPI) — voir STACK.md
- kind vs minikube pour le cluster local (S4)
- Auth : session serveur vs JWT basique (rester simple, pas d'OAuth)

---
*Last updated: 2026-06-03*
