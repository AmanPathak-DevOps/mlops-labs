# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a collection of standalone MLOps demo projects, each demonstrating a different deployment pattern for an intent-classification ML model. Projects are independent — changes in one do not affect others.

## Project Layout

| Directory | Purpose |
|-----------|---------|
| `intent-classifier-model/` | Base project: trains a scikit-learn model and serves it via Flask |
| `intent-classifier-model-deploy-kubernetes/` | Same model deployed to Kubernetes (EKS) with Terraform-provisioned infra |
| `intent-classifier-model-deploy-virtual-machine/` | VM/EC2 deployment using gunicorn + wsgi.py |
| `configure-kserve/` | KServe InferenceService deployment on a KinD cluster |
| `experiment_tracking_with_mlflow/` | MLflow experiment tracking with Helm chart (PostgreSQL backend) |
| `wine_prediction_dvc_s3_demo/` | DVC + S3 data versioning demo |
| `first_demo_flowers/` | Iris classification demo, auto-trains on startup |

## Common Commands

### Local Development (per project)

```bash
# Setup (run from inside a project directory)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Train the model (creates artifacts in model/artifacts/)
python model/train.py

# Start the Flask API
python app.py
```

### Docker

```bash
# Build image (each project has its own Dockerfile)
docker build -t <image-name> .

# Run container
docker run -p 5000:5000 <image-name>
```

**Note:** Model training happens at Docker build time (`RUN python3 model/train.py` in Dockerfile), so the artifact is baked into the image.

### Kubernetes (intent-classifier-model-deploy-kubernetes)

```bash
# Apply all manifests
kubectl apply -f kubernetes-manifests/

# Verify deployment
kubectl get pods -n mlops-projects
kubectl get svc -n mlops-projects
```

### Terraform (EKS infra)

```bash
cd intent-classifier-model-deploy-kubernetes/infra-eks-terraform/
terraform init
terraform plan
terraform apply
```

### MLflow Helm Chart

```bash
cd experiment_tracking_with_mlflow/mlflow-installation/
helm install mlflow ./mlflow-helmchart -f mlflow-helmchart/values.yaml

# Set tracking URI for experiment scripts
export MLFLOW_TRACKING_URI=http://localhost:5000
python experiment_tracking_with_mlflow/wine_quality_experiment.py
```

### Testing API Endpoints

```bash
# Intent classifier (port 5000 or 6000)
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "book a flight"}'

# Flowers demo (port 5001)
curl -X POST http://127.0.0.1:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### DVC (wine_prediction_dvc_s3_demo)

```bash
dvc pull   # fetch data from S3
dvc push   # push data to S3
dvc repro  # reproduce pipeline
```

## Architecture

### ML Model Stack

- **Algorithm:** scikit-learn `MultinomialNB` wrapped in a `Pipeline` (CountVectorizer → NaiveBayes)
- **Serialization:** `joblib` pickle files in `model/artifacts/`
- **Serving:** Flask REST API with a `/predict` POST endpoint
- **Production WSGI:** gunicorn (used in VM and Kubernetes deployments)

### Deployment Patterns (same model, three deployment targets)

1. **Kubernetes (EKS):** 2-replica Deployment → ClusterIP Service → Traefik Ingress. Namespace: `mlops-projects`. Image pulled from Docker Hub (`avian19/mlops-intent-project:v2-frontend`).
2. **KServe:** `InferenceService` (v1beta1) using sklearn predictor. Models stored in GCS. Runs on a local KinD cluster.
3. **VM:** Plain gunicorn via `wsgi.py`; no orchestration.

### MLflow Stack (Helm)

- **Chart:** `experiment_tracking_with_mlflow/mlflow-installation/mlflow-helmchart/` (chart version 1.8.1, MLflow image `burakince/mlflow:3.7.0`)
- **Backend store:** PostgreSQL (default) or MySQL
- **Artifact store:** Configurable (local or S3)
- **Extras:** HPA, Ingress, ServiceAccount, RBAC, non-root security context (runAsUser: 1001)

### KServe Setup

See `configure-kserve/sample-kserve/KSERVER_INSTALLATIONS_INSTRUCTIONS.md` for the full step-by-step KinD cluster + KServe installation guide.

## Port Reference

| Project | Port |
|---------|------|
| intent-classifier (local/K8s) | 5000 |
| intent-classifier (alt) | 6000 |
| first_demo_flowers | 5001 |
| MLflow tracking server | 5000 |

## Key Dependencies

```
scikit-learn==1.3.2
Flask==2.3.2
joblib
gunicorn
mlflow==3.12.0   # experiment_tracking_with_mlflow only
dvc==3.67.1      # wine_prediction_dvc_s3_demo only
dvc-s3
```
