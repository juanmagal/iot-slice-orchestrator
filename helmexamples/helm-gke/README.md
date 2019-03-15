
Configure GKE cluster

gcloud init
gcloud config list
gcloud container clusters get-credentials <cluster-name>
  
Install Helm in cluster

kubectl create serviceaccount --namespace kube-system tiller
helm init --service-account tiller
kubectl create clusterrolebinding tiller-cluster-role --clusterrole=cluster-admin --serviceaccount=kube-system:tiller

