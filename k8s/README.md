# Déploiement Kubernetes local — Forum DevOps

Manifests de déploiement du forum sur un cluster Kubernetes local (**minikube**).

> Choix minikube vs kind : **minikube** retenu pour son écosystème d'addons
> intégrés (ingress, metrics-server) qui accélère le déploiement local et le
> monitoring (Phase 5) sans configuration manuelle.

## Architecture déployée

```
  (minikube tunnel)         namespace: forum
        │
   ┌────▼─────────┐    ┌──────────────┐    ┌────────────────────┐
   │   Ingress    │───▶│ Service api  │───▶│ Deployment api      │
   │ forum.local  │    │ (ClusterIP)  │    │ + initContainer     │
   └──────────────┘    └──────────────┘    │   (alembic migrate) │
                                           └─────────┬──────────┘
                                           ┌─────────▼──────────┐
                                           │ Service db (headless)│
                                           │ StatefulSet db + PVC │
                                           └──────────────────────┘
```

| Fichier | Ressource | Rôle |
|---------|-----------|------|
| `00-namespace.yaml`     | Namespace            | Isole l'app dans `forum` |
| `01-configmap.yaml`     | ConfigMap            | Config non sensible (user, db, port) |
| `examples/secret.example.yaml`| Secret (gabarit) | Modèle hors apply — **sans valeurs réelles** |
| `10-db-statefulset.yaml`| StatefulSet + PVC    | PostgreSQL persistant |
| `11-db-service.yaml`    | Service headless     | DNS interne `db:5432` |
| `20-api-deployment.yaml`| Deployment           | API FastAPI + migration (initContainer) |
| `21-api-service.yaml`   | Service ClusterIP    | DNS interne `api:8000` |
| `30-ingress.yaml`       | Ingress              | Entrée HTTP `forum.local` |
| `40-grafana-datasource.yaml` | ConfigMap | Provisionne une datasource Prometheus pour Grafana |
| `41-grafana-dashboard-configmap.yaml` | ConfigMap | Provisionne un dashboard Grafana pour le service forum |
| `42-grafana-deployment.yaml` | Deployment | Grafana avec provisionneur de dashboards |
| `43-grafana-service.yaml` | Service | Expose Grafana sur le cluster |
| `44-grafana-ingress.yaml` | Ingress | Accès Grafana `grafana.local` |

## Prérequis

- Docker en cours d'exécution
- `kubectl` et `minikube` installés (`brew install minikube`)
- Image API construite : `docker compose build` (produit `devops-fil-rouge-template-api:latest`)

## Déploiement complet

```bash
# 1. Cluster (04-01)
minikube start --driver=docker --profile=forum
minikube addons enable ingress --profile=forum

# 2. Charger l'image API locale dans le cluster
minikube image load devops-fil-rouge-template-api:latest --profile=forum

# 3. Préparer le secret réel (NON versionné)
cp k8s/examples/secret.example.yaml k8s/02-secret.yaml
#   → éditer k8s/02-secret.yaml avec les vraies valeurs

# 4. Appliquer tous les manifests (l'ordre 00→30 est garanti par le tri)
kubectl --context forum apply -f k8s/

# 5. Attendre que tout soit prêt
kubectl --context forum -n forum rollout status deployment/api
echo "Waiting for Grafana..."
kubectl --context forum -n forum rollout status deployment/grafana
```

## Accès à l'application

**Méthode 1 — Ingress (recommandée).** Sur macOS/driver Docker, l'IP du cluster
n'est pas joignable directement : utiliser `minikube tunnel`.

```bash
sudo minikube tunnel --profile=forum     # laisse tourner dans un terminal
echo "127.0.0.1 forum.local" | sudo tee -a /etc/hosts
curl http://forum.local/health           # {"status":"ok"}
```

## Accès à Grafana

```bash
sudo minikube tunnel --profile=forum
echo "127.0.0.1 grafana.local" | sudo tee -a /etc/hosts
curl http://grafana.local
```

- URL Grafana : `http://grafana.local`
- Login : `admin`
- Password : `admin`

Le dashboard est provisionné automatiquement via les manifests Kubernetes.

**Méthode 2 — port-forward (rapide, sans tunnel).**

```bash
kubectl --context forum -n forum port-forward svc/api 8000:8000
curl http://localhost:8000/health
# Swagger : http://localhost:8000/docs
```

## Vérification

```bash
kubectl --context forum -n forum get pods,svc,ingress,pvc
# Tables en base :
kubectl --context forum -n forum exec db-0 -- psql -U forum_user -d forum -c "\dt"
```

## Cycle de vie

```bash
minikube stop  --profile=forum   # arrêter (garde l'état + le PVC)
minikube start --profile=forum   # redémarrer
kubectl --context forum delete namespace forum   # tout supprimer (app)
minikube delete --profile=forum                  # supprimer le cluster
```

---
*Manifests Lead Ops — Phase 4 (S4) : 04-01 cluster · 04-02 api · 04-03 db · 04-04 ingress.*
