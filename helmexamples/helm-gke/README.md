
### 1. Configure GKE cluster
```
gcloud init
gcloud config list
gcloud container clusters get-credentials <cluster-name>
```
### 2. Install Helm in cluster
```
kubectl create serviceaccount --namespace kube-system tiller
helm init --service-account tiller
kubectl create clusterrolebinding tiller-cluster-role --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
```
### 3. Install NFS disk
```
gcloud compute disks create --size=10GB --zone=us-east1-b gce-nfs-disk
kubectl create namespace nfs
kubectl apply -n nfs -f k8s/nfs-server.yaml
```
### 4. Install NATS cluster (for Mainflux)
```
helm install --namespace nats-io helmexamples/helm/nats/
```
### 5. Iotorch commands 

Get ip and context from config view data and helm ip from services data (note it must be exposed)
GOOGLE_APPLICATION_CREDENTIALS must be properly settled.

``` 
kubectl get services --all-namespaces
kubectl config view
iotorch k8scluster create --name=gke --ip=<cluster-ip> --k8shelmport=44134 --k8scontext=<cluster-context> --k8shelmip=<helm-ip>
iotorch iotslice create --name=<slice-name> --edge gke --cloud gke
iotorch iotserver create --name <server-name> --cluster=gke --slice=<slice-name> --helmpath=./helmexamples/helm/mainflux/
```
