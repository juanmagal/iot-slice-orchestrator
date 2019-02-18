# iot-slice-orchestrator
Orchestrator of iot slices implemented in python

Purpose
-------

This is a CLI application to orchestrate IoT slices in Kubernetes clusters deployed at the edge or in the cloud.

Apart from creating slices, it is possible to deploy an IoT Gateway (EdgeX) and an IoT Server (Mainflux) in a given slice and in a Kubernetes cluster. IoT Gateway can be attached to an IoT Server to forward the requests received from the IoT devices, so that they can be later processed.

It is also possible to define IoT Devices and connect them to IoT Gateway, so far only MQTT protocol is supported for this purpose.


Installation
------------

In order to install the library (*and all development dependencies*), run the following command:

    $ pip install -e .[test]

Usage
-----

The following commands can be executed:

For configuration of Kubernetes clusters where IoT Gateways and Servers will be deployed:

    $ iotorch k8scluster create --name=<name> [--ip=<ipaddress>] [--k8scontext=<context>] [--k8shelmport=<port>]
    $ iotorch k8scluster delete --name=<name>
    $ iotorch k8scluster get --name=<name>
    $ iotorch k8scluster list

For definition of IoT Slices:

    $ iotorch iotslice create --name=<name> --edge=<k8cluster> --cloud=<k8cluster>
    $ iotorch iotslice delete --name=<name>
    $ iotorch iotslice get --name=<name>
    $ iotorch iotslice list

In order to manager IoT Servers:

    $ iotorch iotserver create --name=<name> --cluster=<k8scluster> [--slice=<iotslice>] [--helmpath=<path>]
    $ iotorch iotserver delete --name=<name>
    $ iotorch iotserver get --name=<name>
    $ iotorch iotserver list

In order to manage IoT Gateways :

    $ iotorch iotgateway create --name=<name> --cluster=<k8cluster> [--slice=<iotslice>] [--helmpath=<path>]
    $ iotorch iotgateway attach --name=<name> --server=<iotserver>
    $ iotorch iotgateway delete --name=<name>
    $ iotorch iotgateway get --name=<name>
    $ iotorch iotgateway list

To handle IoT Devices and attach them to an IoT Gateway:

    $ iotorch iotdevice create --name=<name> [--gateway=<iotgateway>]
    $ iotorch iotdevice delete --name=<name>
    $ iotorch iotdevice get --name=<name>
    $ iotorch iotdevice list

Example
-------
Examples of iotorch commands:

    iotorch k8scluster create --name=edgecluster --k8scontext=edgecluster-context --ip=10.10.10.10 --k8shelmport=44134
    iotorch k8scluster create --name=cloudcluster --k8scontext=cloudcluster-context --ip=10.10.10.11 --k8shelmport=44134
    iotorch iotslice create --name=testslice --edge=edgecluster --cloud=cloudcluster
    iotorch iotgateway create --name gwtest --cluster=edgecluster --slice=testslice --helmpath=/home/helm/gatewaychart
    iotorch iotserver create --name=servertest --cluster=cloudcluster --slice=testslice --helmpath=/home/helm/serverchart
    
    iotorch iotserver delete --name=servertest
    iotorch iotgateway delete --name gwtest
    iotorch iotslice delete --name=testslice
    iotorch k8scluster delete --name=edgecluster
    iotorch k8scluster delete --name=cloudcluster

Initial Configuration
---------------------
In order to manager different Kubernetes clusters, different contexts must be defined following [kubernetes documentation](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/). Note iotorch will set the right context depending on the cluster to use.

One way of doing that is by setting different Kubernetes config files in ``KUBECONFIG`` variable:

    export  KUBECONFIG=$KUBECONFIG:<cluster1_config_file_path>:<cluster2_config_file_path>

It is important to notice same cluster names, context names and user names should not be used for all config files. This is an example of a configuration with two different contexts:

    > kubectl config view
    
    apiVersion: v1
    clusters:
    - cluster:
        certificate-authority-data: DATA+OMITTED
        server: https://edgecluster:6443
      name: edgecluster
    - cluster:
        certificate-authority-data: DATA+OMITTED
        server: https://cloudcluster:6443
      name: cloudcluster
    contexts:
    - context:
        cluster: edgecluster
        user: edgecluster-admin
      name: edgeclustercontext
    - context:
        cluster: cloudcluster
        user: cloudcluster-admin
      name: cloudclustercontext
    current-context: cluster2
    kind: Config
    preferences: {}
    users:
    - name: edgecluster-admin
      user:
        client-certificate-data: REDACTED
        client-key-data: REDACTED
    - name: cloudcluster-admin
      user:
        client-certificate-data: REDACTED
        client-key-data: REDACTED

Configuration
-------------
All the configuration of the system is stored in a toml file, whose name by default is ``iotorch.toml`` and by default is stored in the same folder where the commands are executed.

This is a fairly complete initial configuration example:

    title = "Example of IoT Orchestrator Configuration"
    
    # List of IoT devices
    [iotdevices]
        [iotdevice.test]
        gateway = "test"
    
    # List of configured kubernetes clusters
    [k8sclusters]
        [k8scluster.test]
        ip = "127.0.0.1"
   
    # List of IoT slices
    [iotslices]
        [iotslice.test]
        edge = "test"
        cloud = "test"
    
    # List of IoT Gateways
    [iotgateways]
        [iotgateway.test]
        slice = "test"
        cluster = "test"
    
    # List of IoT Servers
    [iotservers]
        [iotserver.test]
        slice = "test"
        cluster = "test"
        
Testing
-------
Execute the following command to execute all tests

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.
