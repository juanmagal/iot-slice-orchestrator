"""Tests for our `iotorch IoT Gateway` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestIotGateway(TestCase):

    def test_returns_iotgateway_create(self):
        name='gateway1'
        cluster='cluster1'
        iotslice='slice1'
        operation='create'
        text= 'Creating IoT Gateway: ' + name + ' ' + cluster + ' ' + iotslice
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_attach(self):
        name='gateway1'
        server='server1'
        operation='attach'
        text= 'Attaching IoT Gateway: ' + name + ' to IoT Server ' + server
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--server='+server], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_delete(self):
        name='gateway1'
        operation='delete'
        text='Deleting IoT Gateway: ' + name
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_get(self):
        name='test'
        operation='get'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotgateway_get_file_does_not_exit(self):
        name='test'
        operation='get'
        text='Nothing to get'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_list(self):
        name='test'
        operation='list'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotgateway', operation, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotgateway_list_file_does_not_exist(self):
        name='test'
        operation='list'
        text='Nothing to list'
        output = popen(['iotorch', 'iotgateway', operation], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

