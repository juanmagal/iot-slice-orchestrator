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

    $ iotorch k8scluster create --name=<name> --ip=<ipaddress>
    $ iotorch k8scluster delete --name=<name>
    $ iotorch k8scluster get --name=<name>
    $ iotorch k8scluster list

For definition of IoT Slices:

    $ iotorch iotslice create --name=<name> --edge=<k8cluster> --cloud=<k8cluster>
    $ iotorch iotslice delete --name=<name>
    $ iotorch iotslice get --name=<name>
    $ iotorch iotslice list

In order to manager IoT Servers:

    $ iotorch iotserver create --name=<name> --cluster=<k8scluster> [--slice=<iotslice>]
    $ iotorch iotserver delete --name=<name>
    $ iotorch iotserver get --name=<name>
    $ iotorch iotserver list

In order to manage IoT Gateways :

    $ iotorch iotgateway create --name=<name> --cluster=<k8cluster> [--slice=<iotslice>]
    $ iotorch iotgateway attach --name=<name> --server=<iotserver>
    $ iotorch iotgateway delete --name=<name>
    $ iotorch iotgateway get --name=<name>
    $ iotorch iotgateway list

To handle IoT Devices and attach them to an IoT Gateway:

    $ iotorch iotdevice create --name=<name> [--gateway=<iotgateway>]
    $ iotorch iotdevice delete --name=<name>
    $ iotorch iotdevice get --name=<name>
    $ iotorch iotdevice list

Initial Configuration
---------------------

It is possible to define the initial configuration of the system by creating a toml file, whose name by default is ``iotorch.toml`` and shall be located in the same folder from which iotorch commands will be called.
This is a fairly complete initial configuration example:

    title = "Example of IoT Orchestrator Configuration"
    
    # List of IoT devices
    [iotdevices]
        [iotdevice.test]
        name = "test"
        gateway = "test"
    
    # List of configured kubernetes clusters
    [k8sclusters]
        [k8scluster.test]
        name = "test"
        ip = "127.0.0.1"
   
    # List of IoT slices
    [iotslices]
        [iotslice.test]
        name = "test"
        edge = "test"
        cloud = "test"
    
    # List of IoT Gateways
    [iotgateways]
        [iotgateway.test]
        name = "test"
        slice = "test"
        cluster = "test"
    
    # List of IoT Servers
    [iotservers]
        [iotserver.test]
        name = "test"
        slice = "test"
        cluster = "test"
        
Testing
-------
Execute the following command to execute all tests

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.
