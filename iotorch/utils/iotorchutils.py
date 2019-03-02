import toml

K8S_CLUSTERS_KEY = 'k8sclusters'
K8S_CLUSTER_CONTEXT_ATTR = 'k8scontext'
K8S_CLUSTER_IP_ATTR = 'ip'
K8S_CLUSTER_HELM_PORT_ATTR = 'helmport'
K8S_CLUSTER_HELM_IP_ATTR = 'helmip'


def getk8sclustercontext(cluster,config_path):

   with open(config_path) as f:
       config = toml.load(f)
       f.close

   clusters = config.get(K8S_CLUSTERS_KEY)
   if clusters == None:
      return None

   cluster = clusters.get(cluster)
   if cluster == None:
      return None

   return cluster.get(K8S_CLUSTER_CONTEXT_ATTR) 


def getk8sclusterip(cluster,config_path):

   with open(config_path) as f:
       config = toml.load(f)
       f.close

   clusters = config.get(K8S_CLUSTERS_KEY)
   if clusters == None:
      return None

   cluster = clusters.get(cluster)
   if cluster == None:
      return None

   return cluster.get(K8S_CLUSTER_IP_ATTR)   

def getk8sclusterhelmport(cluster,config_path):

   with open(config_path) as f:
       config = toml.load(f)
       f.close

   clusters = config.get(K8S_CLUSTERS_KEY)
   if clusters == None:
      return None

   cluster = clusters.get(cluster)
   if cluster == None:
      return None

   return cluster.get(K8S_CLUSTER_HELM_PORT_ATTR)

def getk8sclusterhelmip(cluster,config_path):

   with open(config_path) as f:
       config = toml.load(f)
       f.close

   clusters = config.get(K8S_CLUSTERS_KEY)
   if clusters == None:
      return None

   cluster = clusters.get(cluster)
   if cluster == None:
      return None

   return cluster.get(K8S_CLUSTER_HELM_IP_ATTR)
