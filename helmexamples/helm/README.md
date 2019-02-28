# Deploy Mainflux on Kubernetes - WIP
Scripts to deploy Mainflux on Kubernetes (https://kubernetes.io) using Helm (https://helm.sh/). Work in progress. Not ready for deployment.

## Steps

### 0. Install helm

- To install helm, follow [HELM user guide](https://docs.helm.sh/using_helm/)

### 1. Setup NATS

- To setup NATS cluster on k8s we recommend using [NATS operator](https://github.com/nats-io/nats-operator/tree/master/helm/nats-operator). NATS cluster should be deployed on namespace `nats-io`.

- A simplified example for small deployments is included in nats folder, in that case the following commands shall be executed:
```
kubectl create namespace nats-io

helm install --namespace nats-io nats/

```

### 2. Install mainflux

- Mainflux can be installed using the following command

```
helm install --namespace <whatever> mainflux/
```

<span style="color:red">Istio part has been obviated for now, Nginx still used </span>

Default values can be changed by updating values files, by passing a new values file to helm install or by directly setting the parameter values as part of helm install command. For more information see [HELM user guide](https://docs.helm.sh/using_helm/)


### 3. Install Grafana

- Deploy Grafana 

```
helm install --namespace <whatever> grafana/
```

### 4. Create MetalLB  L2 Load Balancer to provide external access to Mainflux Services (optional)

When deploying in baremetal systems, an L2 Load Balancer can be installed. For more information see [MetalLB L2 tutorial](https://metallb.universe.tf/tutorial/layer2/)

```
kubectl apply -f k8s/metallb/metallb.yaml

kubectl apply -f k8s/metallb/layer2-config.yaml
```

### 5. Configure Internet access
Configure NAT on your Firewall to forward ports 80 (HTTP) and 443 (HTTPS) to nginx ingress service

