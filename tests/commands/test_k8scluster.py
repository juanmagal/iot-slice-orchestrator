"""Tests for our `iotorch k8scluster` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestK8sCluster(TestCase):

    def test_returns_k8scluster_create(self):
        output = popen(['iotorch', 'k8scluster', 'create'], stdout=PIPE).communicate()[0]
        self.assertTrue('Creating k8s cluster!'.encode('utf-8') in output)

    def test_returns_k8scluster_delete(self):
        output = popen(['iotorch', 'k8scluster', 'delete'], stdout=PIPE).communicate()[0]
        self.assertTrue('Deleting k8s cluster!'.encode('utf-8') in output)
