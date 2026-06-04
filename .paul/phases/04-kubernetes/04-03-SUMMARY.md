---
phase: 04-kubernetes
plan: 03
type: execute
status: done
owner: Lead Ops (Baptiste Baudry)
completed: 2026-06-04
---

# SUMMARY 04-03 — Base PostgreSQL (StatefulSet + PVC)

## Objectif
Déployer PostgreSQL dans le cluster avec une persistance stable.

## Réalisé
- `k8s/10-db-statefulset.yaml` : **StatefulSet** `postgres:16-alpine`, 1 replica,
  `volumeClaimTemplates` → **PVC 1Gi** (persistance). `PGDATA` en `subPath` pour éviter
  l'erreur « data directory not empty ». Probes readiness/liveness via `pg_isready`.
- `k8s/11-db-service.yaml` : **Service headless** `db` → DNS interne stable `db:5432`.
- `k8s/01-configmap.yaml` : config non sensible (`POSTGRES_USER`, `POSTGRES_DB`, `PORT`).
- `k8s/examples/secret.example.yaml` : gabarit Secret **sans valeurs** ; vrai
  `k8s/02-secret.yaml` **gitignoré**.

## Décisions
- **StatefulSet (pas Deployment)** pour la DB : identité + stockage stables, PVC
  ré-attaché au même pod → persistance survit aux redéploiements (boundary ARCHITECTURE.md).

## Vérifié
- Pod `db-0` Running 1/1, PVC `pgdata-db-0` **Bound** 1Gi.

## Fichiers
- `k8s/01-configmap.yaml`, `k8s/10-db-statefulset.yaml`, `k8s/11-db-service.yaml`,
  `k8s/examples/secret.example.yaml`
