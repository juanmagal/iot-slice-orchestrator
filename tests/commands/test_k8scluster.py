"""Tests for our `iotorch k8scluster` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestK8sCluster(TestCase):

    def test_returns_k8scluster_create(self):
        name='cluster1'
        ipaddress='127.0.0.1'
        operation='create'
        text= 'Creating k8s cluster: ' + name + ' ' + ipaddress
        output = popen(['iotorch', 'k8scluster', operation, '--name='+name, '--ip='+ipaddress],stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_k8scluster_create_wrong_ip_address(self):
        name='cluster1'
        ipaddress='wrong'
        operation='create'
        text= 'Wrong IP Address format'
        output = popen(['iotorch', 'k8scluster', operation, '--name='+name, '--ip='+ipaddress],stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_k8scluster_delete(self):
        operation='delete'
        name='cluster1'
        text= 'Deleting k8s cluster: ' + name
        output,error = popen(['iotorch', 'k8scluster', operation, '--name='+name], stdout=PIPE).communicate()
        self.assertTrue(text.encode('utf-8') in output)


