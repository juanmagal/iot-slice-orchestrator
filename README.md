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

* For configuration Kubernetes clusters where IoT Gateways and Servers will be deployed:

    $ pip install -e .[test]


Testing
-------
Execute the following command to execute all tests

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.
