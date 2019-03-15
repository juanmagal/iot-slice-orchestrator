
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
