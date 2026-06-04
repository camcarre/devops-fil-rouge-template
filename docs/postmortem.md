# Post-mortem Phase 5 — Monitoring + Security Scan

## Contexte

La Phase 5 du fil rouge vise à compléter l’application forum par une observabilité opérationnelle et une revue sécurité de base. Le but est d’ajouter une exposition métrique, un monitoring avec Grafana, un scan d’image, et une documentation de retour d’expérience.

## Objectifs

- 05-01 : Exposer des métriques applicatives via `/metrics` et Prometheus
- 05-02 : Provisionner des dashboards Grafana pertinents pour l’API
- 05-03 : Intégrer un scan de sécurité image + un audit dépendances dans la CI
- 05-04 : Documenter les choix, incidents et limites dans un post-mortem

## Livrables réalisés

- `src/main.py` : ajout d’un middleware Prometheus et d’un endpoint `/metrics`
- `tests/test_metrics.py` : validation de l’exposition des métriques
- `requirements.txt` / `requirements-dev.txt` : ajout de `prometheus-client` et `pip-audit`
- `k8s/40-grafana-datasource.yaml` à `k8s/44-grafana-ingress.yaml` : manifests Grafana et dashboard
- `k8s/README.md` : documentation d’accès Grafana et déploiement K8s
- `.github/workflows/ci.yml` : job `security-scan` Trivy + étape `pip-audit`
- `.paul/ROADMAP.md`, `.paul/PROJECT.md`, `.paul/STATE.md`, `README.md` : mise à jour de l’état du projet

## Incidents et apprentissages

- Branching par sous-phase a permis d’isoler chaque livrable et de ne pas mélanger monitoring, dashboards, scan et documentation.
- La répétition de vérification de branche était utile pour rester aligné avec le bon contexte de travail.
- L’ajout d’une étape `pip-audit` dans la CI renforce la revue dépendances sans bloquer le build principal.
- Le scan Trivy est configuré pour échouer sur vulnérabilités `HIGH` ou `CRITICAL`, ce qui apporte une règle de qualité stricte.

## Choix techniques

- `prometheus-client` est utilisé côté application pour générer des métriques standard Prometheus.
- L’exportateur `/metrics` est exposé dans la même application FastAPI, ce qui simplifie le déploiement et le scrape Prometheus.
- Grafana est provisionné via des `ConfigMap` Kubernetes, ce qui permet de créer automatiquement la datasource et le dashboard lors du déploiement.
- Le dashboard couvre :
  - le taux de requêtes HTTP par chemin
  - la latence 95e percentile par chemin
- `Trivy` est installé dans le workflow CI à partir du script officiel pour scanner l’image locale construite.
- `pip-audit` est exécuté dans le job de lint/test pour détecter les dépendances vulnérables au niveau Python.

## Limites

- Le monitoring est pensé pour un cluster local minikube et n’est pas encore industrialisé pour un environnement de production.
- Le dashboard Grafana est basique et couvre uniquement les métriques applicatives ; aucun dashboard DB dédié n’a été ajouté.
- La sécurité reste un niveau de revue de base : audit de dépendances et scan d’image, sans politique d’infrastructure ou de conteneurs renforcée.
- La persistance de Grafana n’est pas gérée ici ; le déploiement reste non productif.

## Recommandations S6

- Préparer la présentation en montrant :
  - l’API qui répond sur `/health`
  - l’endpoint `/metrics` et le contenu Prometheus
  - le dashboard Grafana accessible via `grafana.local`
  - le pipeline GitHub Actions incluant le scan Trivy
- Documenter la façon de lancer le cluster minikube et les commandes de vérification.
- Fusionner les branches de Phase 5 dans `master` après revue.

## Fichiers clés

- `src/main.py`
- `tests/test_metrics.py`
- `requirements-dev.txt`
- `k8s/40-grafana-datasource.yaml`
- `k8s/41-grafana-dashboard-configmap.yaml`
- `k8s/42-grafana-deployment.yaml`
- `k8s/43-grafana-service.yaml`
- `k8s/44-grafana-ingress.yaml`
- `.github/workflows/ci.yml`
- `.paul/ROADMAP.md`
- `.paul/PROJECT.md`
- `.paul/STATE.md`
- `README.md`
