# This Guide will help you to configure Kserve on your Kubernetes Cluster(I am deploying Kserve CRD on KinD cluster)

## Install Helm (Pre-requisites)
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
chmod 700 get_helm.sh
./get_helm.sh
```

## Install cert-manager (Pre-requisites)
```
helm install \
  cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --version v1.20.2 \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```

## Install KServe CRD [[text](https://kserve.github.io/website/docs/admin-guide/kubernetes-deployment)]
```
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.18.0
```

## Install KServe using Helm Chart
```
helm install kserve oci://ghcr.io/kserve/charts/kserve-resources --version v0.18.0 \
  --set kserve.controller.deploymentMode=Standard \
  --set kserve.controller.gateway.ingressGateway.enableGatewayApi=true \
  --set kserve.controller.gateway.ingressGateway.kserveGateway=kserve/kserve-ingress-gateway
```

## Instal the Kserve Runtimes
```
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.18.0/kserve-cluster-resources.yaml
kubectl get clusterservingruntimes
```

## Deploy the Inference Service
```
kubectl apply -f inference_svc.yaml
```

## List all the resources created by IS including Ingress
```
kubectl get all -n mlops-projects
kubectl get ing -n mlops-projects
```

## Port forward to access your model application
```
kubectl port-forward -n mlops-projects service/sklearn-iris-predictor 8080:80
```

## Use CURL command to access the Model
```
curl -s -H "Content-Type: application/json"   -d '{"instances":[[10.5,2.3,4,2]]}' http://localhost:8080/v1/models/sklearn-iris:predict | jq
curl -s -H "Content-Type: application/json"   -d '{"instances":[[10.5,2.33,40.2,2]]}' http://localhost:8080/v1/models/sklearn-iris:predict | jq
curl -s -H "Content-Type: application/json"   -d '{"instances":[[0.5,2.33,0.2,2]]}' http://localhost:8080/v1/models/sklearn-iris:predict | jq
```
