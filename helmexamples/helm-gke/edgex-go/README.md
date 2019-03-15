# edgex-on-kubernetes using Helm - WIP
Deploying EdgeX on Kubernetes (https://kubernetes.io) using Helm. Work in progress. Not ready for deployment.

## Steps

### 1. Install MetalLB in case we need to deploy it in a bare-metal K8s cluster

For more information see [MetalLB L2 tutorial](https://metallb.universe.tf/tutorial/layer2/)

```
kubectl apply -f k8s/metallb/metallb.yaml

kubectl apply -f k8s/metallb/layer2-config.yaml

### 2. Install EdgeX Kubernetes Helm Chart

helm install .

### 3. Configure Internet access
Configure NAT on your Firewall to forward port 1883 (MQTT)

