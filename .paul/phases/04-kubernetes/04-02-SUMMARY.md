---
phase: 04-kubernetes
plan: 02
type: execute
status: done
owner: Lead Ops (Baptiste Baudry)
completed: 2026-06-04
---

# SUMMARY 04-02 — API (Deployment + Service + migration initContainer)

## Objectif
Déployer l'API FastAPI dans le cluster, connectée à la DB, migrations appliquées.

## Réalisé
- Image locale `devops-fil-rouge-template-api:latest` chargée dans le cluster
  (`minikube image load`), `imagePullPolicy: IfNotPresent` (pas de pull registry).
- `k8s/20-api-deployment.yaml` : **Deployment** stateless 1 replica.
  - **initContainer `migrate`** : `alembic upgrade head` avant le démarrage d'uvicorn.
  - `DATABASE_URL` construit depuis ConfigMap + Secret via `$(VAR)`, cible `db:5432`.
  - Probes readiness/liveness sur `/health`.
- `k8s/21-api-service.yaml` : **Service ClusterIP** `api` (exposition externe en 04-04).

## Décisions
- **Deployment (pas StatefulSet)** : API stateless, tout l'état en DB → scalable/redéployable.
- **initContainer pour la migration** : sépare « préparer le schéma » de « servir ».

## Vérifié
- Rollout OK ; logs initContainer : `Running upgrade -> 001`.
- Via port-forward : `/health` → 200, inscription → 201 (user persisté), 4 tables en base.

## Fichiers
- `k8s/20-api-deployment.yaml`, `k8s/21-api-service.yaml`
