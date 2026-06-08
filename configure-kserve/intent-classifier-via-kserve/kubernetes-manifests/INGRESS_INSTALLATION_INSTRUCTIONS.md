# This Guide will help you to configure Traefik on your Kubernetes Cluster(I am deploying Traefik on EKS(AWS))

## Install Helm (Pre-requisites)
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
chmod 700 get_helm.sh
./get_helm.sh
```

## Add Traefik Helm repo and create namespace
```
helm repo add traefik https://traefik.github.io/charts
helm repo update
kubectl create namespace traefik
```

## Install Traefik
```
helm install traefik traefik/traefik \
    --namespace traefik \
    --create-namespace
```

## Validate
```
kubectl get pods -n traefik
```

## Get the LoadBalancer DNS
```
kubectl get svc -n traefik
```

