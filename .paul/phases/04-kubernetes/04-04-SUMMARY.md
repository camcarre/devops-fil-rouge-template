---
phase: 04-kubernetes
plan: 04
type: execute
status: done
owner: Lead Ops (Baptiste Baudry)
completed: 2026-06-04
---

# SUMMARY 04-04 — Ingress + accès local + doc de déploiement

## Objectif
Exposer l'API hors du cluster et documenter le déploiement complet.

## Réalisé
- Addon ingress activé : `minikube addons enable ingress`.
- `k8s/30-ingress.yaml` : **Ingress nginx** `forum.local` → service `api:8000`.
- `k8s/README.md` complété : schéma d'architecture, tableau des ressources, déploiement
  pas-à-pas, **deux méthodes d'accès** (`minikube tunnel` + `port-forward`), cycle de vie.
- Correction qualité : gabarit secret déplacé dans `k8s/examples/` pour qu'il ne soit
  **pas appliqué** par `kubectl apply -f k8s/` (évite d'écraser le vrai secret).

## Vérifié
- Ingress obtient une adresse ; routing `forum.local/health` → 200 (testé depuis le nœud).
- `kubectl apply -f k8s/` **idempotent**, ordre 00→30, secret appliqué une seule fois.

## Limite connue
- Sur macOS/driver Docker, l'IP cluster n'est pas joignable directement → `minikube tunnel`
  requis pour l'accès `forum.local` depuis l'hôte (documenté).

## Fichiers
- `k8s/30-ingress.yaml`, `k8s/README.md`, `k8s/examples/secret.example.yaml`
