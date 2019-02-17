import toml

K8S_CLUSTERS_KEY = 'k8sclusters'
K8S_CLUSTER_CONTEXT_ATTR = 'k8scontext'

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

   


