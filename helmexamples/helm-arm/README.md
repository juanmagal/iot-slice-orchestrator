### 1. Deploy Kubernetes cluster

### 2. Install Helm in cluster
```
kubectl create serviceaccount --namespace kube-system tiller
helm init --service-account tiller
kubectl create clusterrolebinding tiller-cluster-role --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
```
### 3. Enable metrics (optional)

``` 
kubectl apply -n slice4 -f helmexamples/helm-gke/k8s/influxdb.yml
kubectl create configmap -n slice4 --from-file helmexamples/helm-gke/k8s/telegraf.conf
kubectl create -n slice4 -f helmexamples/helm-gke/k8s/telegraf.yaml
helm install helmexamples/helm/grafana/
./edgex_registration_influxdb.sh
```

### 6. Iotorch commands 

Get ip and context from config view data and helm ip from services data (note it must be exposed)
GOOGLE_APPLICATION_CREDENTIALS must be properly settled.
Note we are using NFS based persistent volumes in order to allow multi-write-access (not allowed with regular GKE storage). That must be properly configured (mainly ip and mount path) in helm charts and corresponding yaml files using persisten volumes.
