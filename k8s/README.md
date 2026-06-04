# Déploiement Kubernetes local — Forum DevOps

Manifests de déploiement du forum sur un cluster Kubernetes local (**minikube**).

> Choix minikube vs kind : **minikube** retenu pour son écosystème d'addons
> intégrés (ingress, metrics-server) qui accélère le déploiement local et le
> monitoring (Phase 5) sans configuration manuelle.

## Prérequis

- Docker en cours d'exécution
- `kubectl` et `minikube` installés (`brew install minikube`)

## 1. Démarrer le cluster (plan 04-01)

```bash
# Crée un cluster nommé "forum" avec le driver Docker
minikube start --driver=docker --profile=forum

# Vérifier
kubectl --context forum get nodes
```

## 2. Créer le namespace

```bash
kubectl --context forum apply -f k8s/00-namespace.yaml
kubectl --context forum get namespace forum
```

Toutes les ressources du projet vivent dans le namespace **`forum`**.

## Cycle de vie du cluster

```bash
minikube stop  --profile=forum   # arrêter (garde l'état)
minikube start --profile=forum   # redémarrer
minikube delete --profile=forum  # supprimer entièrement
```

---
*Manifests à venir : api (04-02), db + PVC (04-03), ingress (04-04).*
