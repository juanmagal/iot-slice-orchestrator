from kubernetes import client, config
from kubernetes.client.rest import ApiException
from urllib3.exceptions import MaxRetryError

from . import iotorchutils


def createnamespace(iotslice,cluster,configfile):

    contextname=iotorchutils.getk8sclustercontext(cluster,configfile)
 
    if contextname == None:
       print ("Context for cluster %s not found" %cluster)
       return False

    config.load_kube_config(context=contextname)
    v1 = client.CoreV1Api()

    namespace = client.V1Namespace(
        api_version="v1",
        kind="Namespace",
        metadata=client.V1ObjectMeta(name=iotslice))

    # Create namespace

    try:
       api_response = v1.create_namespace(body=namespace)
    except ApiException as ae:
       print ("Error creating namespace, %s" %ae.reason)
       return False
    except MaxRetryError as me:
       print ("Error creating namespace, %s" %me.reason)
       return False

    return True

def deletenamespace(iotslice,cluster,configfile):

    contextname=iotorchutils.getk8sclustercontext(cluster,configfile)

    if contextname == None:
       print ("Context for cluster %s not found" %cluster)
       return False

    config.load_kube_config(context=contextname)

    v1 = client.CoreV1Api()

    deleteoptions = client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5)

    # Delete namespace

    try:
       api_response = v1.delete_namespace(name=iotslice,body=deleteoptions)
    except ApiException as ae:
       print ("Error deleting namespace, %s" %ae.reason)
       return False
    except MaxRetryError as me:
       print ("Error deleting namespace, %s" %me.reason)
       return False

    return True
