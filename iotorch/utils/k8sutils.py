from kubernetes import client, config
from kubernetes.client.rest import ApiException
from urllib3.exceptions import MaxRetryError

from pyhelm.chartbuilder import ChartBuilder
from pyhelm.tiller import Tiller


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

def createhelmincluster(iotslice,cluster,helmpath,configfile,name):

    clusterip=iotorchutils.getk8sclusterip(cluster,configfile)

    clusterhelmport=iotorchutils.getk8sclusterhelmport(cluster,configfile)

    if clusterip == None:
       print ("IP Address for cluster %s not found" %cluster)
       return False

    releasename = name+"-"+iotslice

    chart = ChartBuilder({'name': name, 'source': {'type': 'directory', 'location': helmpath}})

    t = Tiller(host=clusterip,port=clusterhelmport)

    t.install_release(chart.get_helm_chart(), dry_run=False, namespace=iotslice, name=releasename)

    return True

def deletehelmincluster(iotslice,cluster,configfile,name):

    clusterip=iotorchutils.getk8sclusterip(cluster,configfile)

    clusterhelmport=iotorchutils.getk8sclusterhelmport(cluster,configfile)

    t = Tiller(host=clusterip,port=clusterhelmport)

    releasename = name+"-"+iotslice

    t.uninstall_release(release=releasename)

    return True


def createiotgatewayincluster(iotslice,cluster,helmpath,configfile):

    return createhelmincluster(iotslice,cluster,helmpath,configfile,"iotgateway")

def deleteiotgatewayincluster(iotslice,cluster,configfile):

    return deletehelmincluster(iotslice,cluster,configfile,"iotgateway")

def createiotserverincluster(iotslice,cluster,helmpath,configfile):

    return createhelmincluster(iotslice,cluster,helmpath,configfile,"iotserver")

def deleteiotserverincluster(iotslice,cluster,configfile):

    return deletehelmincluster(iotslice,cluster,configfile,"iotserver")

