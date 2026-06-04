# Déploiement Kubernetes local — Forum DevOps

> Manifests de déploiement du forum sur un cluster Kubernetes local (**minikube**).
> Toutes les commandes sont reproductibles en moins de 5 minutes par un tiers.

## Choix d'architecture

- **minikube vs kind** : minikube retenu pour ses addons intégrés
  (`ingress`, `metrics-server`) qui activent le monitoring Prometheus en
  une commande, sans configuration manuelle supplémentaire.
- **StatefulSet + PVC** pour PostgreSQL : le stockage persiste au-delà du pod.
- **initContainer** Alembic : migrations appliquées avant uvicorn.

## Architecture déployée

```
  (minikube tunnel)           namespace: forum
        │
   ┌────▼─────────┐    ┌──────────────┐    ┌──────────────────────┐
   │   Ingress     │───▶│ Service api  │───▶│ Deployment api        │
   │ forum.local   │    │ (ClusterIP)  │    │  FastAPI + uvicorn   │
   │               │    │              │    │  + /health, /metrics │
   └───────────────┘    └──────────────┘    │  + initContainer     │
                                             │  (alembic migrate)   │
                                             └──────────┬───────────┘
                                             ┌──────────▼───────────┐
                                             │ Service db (headless)│
                                             │ StatefulSet db + PVC  │
                                             │ postgres:16-alpine    │
                                             └───────────────────────┘
              Observabilité : /metrics → Prometheus :9090 → Grafana :3000
```

## Fichiers manifests

| Fichier | Ressource | Rôle |
|---------|-----------|------|
| `00-namespace.yaml`     | Namespace | Isole l'app dans `forum` |
| `01-configmap.yaml`     | ConfigMap | Config non sensible (user, db, port) |
| `examples/secret.example.yaml` | Secret (gabarit) | Modèle **jamais appliqué** — valeurs à remplir |
| `10-db-statefulset.yaml`| StatefulSet + PVC | PostgreSQL persistant (1 Gi) |
| `11-db-service.yaml`    | Service headless | DNS interne `db:5432` |
| `20-api-deployment.yaml`| Deployment | API FastAPI + initContainer migrations |
| `21-api-service.yaml`   | Service ClusterIP | DNS interne `api:8000` |
| `30-ingress.yaml`       | Ingress | Entrée HTTP `forum.local` |
| `40-grafana-datasource.yaml` | ConfigMap | Provisionne datasource Prometheus dans Grafana |
| `41-grafana-dashboard-configmap.yaml` | ConfigMap | Provisionne dashboard applicatif |
| `42-grafana-deployment.yaml` | Deployment | Grafana avec provisionneur |
| `43-grafana-service.yaml` | Service | Expose Grafana sur le cluster |
| `44-grafana-ingress.yaml` | Ingress | Accès HTTP `grafana.local` |

## Prérequis

- Docker en cours d'exécution
- `kubectl` installé
- `minikube` ≥ 1.30 installé (`brew install minikube` ou équivalent)
- Image API construite : `docker compose build`

## Démarrage complet (séquence démo — <5 min)

```bash
# 1. Créer / redémarrer le cluster
minikube start --driver=docker --profile=forum
minikube addons enable ingress --profile=forum

# 2. Charger l'image API locale dans le cluster
minikube image load devops-fil-rouge-template-api:latest --profile=forum

# 3. Préparer le secret réel (copie locale — NON versionnée)
cp k8s/examples/secret.example.yaml k8s/02-secret.yaml
# → éditer k8s/02-secret.yaml : remplir POSTGRES_PASSWORD, SECRET_KEY

# 4. Appliquer tous les manifests
kubectl --context forum apply -f k8s/

# 5. Attendre que les déploiements soient prêts
kubectl --context forum -n forum rollout status deployment/api
kubectl --context forum -n forum rollout status deployment/grafana
echo "✓ Déploiement terminé"
```

## Accès à l'API

**Méthode 1 — Ingress (recommandée pour la démo).**
Sur macOS avec le driver Docker, l'IP du cluster n'est pas joignable directement ;
utiliser `minikube tunnel`.

```bash
# Terminal 1 : laisser tourner
sudo minikube tunnel --profile=forum

# Terminal 2 : ajouter au hosts
echo "127.0.0.1 forum.local" | sudo tee -a /etc/hosts

# Tester
curl http://forum.local/healthz
curl http://forum.local/metrics
# Docs Swagger : http://forum.local/docs
```

**Méthode 2 — port-forward (rapide, sans tunnel).**

```bash
kubectl --context forum -n forum port-forward svc/api 8000:8000 &
curl http://localhost:8000/healthz
# Docs Swagger : http://localhost:8000/docs
```

## Accès à Prometheus

```bash
kubectl --context forum -n forum port-forward svc/prometheus 9090:9090 &
# → http://localhost:9090
# Status → Targets : voir que "forum/api" est UP
```

## Accès à Grafana

```bash
# Terminal 1 : tunnel
sudo minikube tunnel --profile=forum

# Terminal 2 : hosts
echo "127.0.0.1 grafana.local" | sudo tee -a /etc/hosts

# → http://grafana.local
# Login : admin / Password : admin
# Dashboard "Forum API" pré-provisionné (requêtes/s, latence p95)
```

**Sans tunnel :**

```bash
kubectl --context forum -n forum port-forward svc/grafana 3000:3000 &
# → http://localhost:3000
```

## Vérification rapide

```bash
# Statut des ressources
kubectl --context forum -n forum get pods,svc,ingress,pvc

# Santé de l'API
curl http://localhost:8000/healthz   # {"status":"ok"}

# Métriques Prometheus
curl http://localhost:8000/metrics  # lines with # HELP http_requests_total

# Tables en base
kubectl --context forum -n forum exec db-0 -- \
  psql -U forum_user -d forum -c "\dt"
```

## Cycle de vie

```bash
# Arrêter le cluster (-garde l'état + PVC)
minikube stop --profile=forum

# Redémarrer
minikube start --profile=forum

# Supprimer uniquement l'application (conserver le cluster)
kubectl --context forum delete namespace forum

# Supprimer le cluster entier
minikube delete --profile=forum
```

---
*Lead Ops — Phase 4 (S4) : 04-01 cluster · 04-02 api · 04-03 db · 04-04 ingress.*
*Phase 5 (S5) : Grafana datasource + dashboard + Ingress.*
