---
phase: 04-kubernetes
plan: 01
type: execute
status: done
owner: Lead Ops (Baptiste Baudry)
completed: 2026-06-04
---

# SUMMARY 04-01 — Cluster local minikube + namespace

## Objectif
Disposer d'un cluster Kubernetes local fonctionnel + un namespace dédié pour isoler l'app.

## Réalisé
- Installation de **minikube** (`brew install minikube`) ; `kubectl` déjà présent.
- Cluster `forum` démarré : `minikube start --driver=docker --profile=forum`.
- `k8s/00-namespace.yaml` : namespace **`forum`** (label `app.kubernetes.io/part-of`).
- `k8s/README.md` : doc de démarrage du cluster + justification du choix.

## Décisions
- **minikube vs kind → minikube** : addons intégrés (ingress, metrics-server) qui
  simplifient l'ingress (04-04) et le monitoring (Phase 5) sans config manuelle.

## Vérifié
- `kubectl --context forum get nodes` → node `forum` Ready (v1.35.1).
- Namespace `forum` Active.

## Fichiers
- `k8s/00-namespace.yaml`, `k8s/README.md`
