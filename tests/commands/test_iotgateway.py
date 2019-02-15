"""Tests for our `iotorch IoT Gateway` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestIotGateway(TestCase):

    def test_returns_iotgateway_get(self):
        name='test'
        operation='get'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotgateway_get_file_does_not_exist(self):
        name='test'
        operation='get'
        configfile='./tests/conf/ghost.toml'
        text='Nothing to get'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_create(self):
        name='gateway1'
        cluster='test1'
        iotslice='test1'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= 'Creating IoT Gateway: ' + name + ' ' + cluster + ' ' + iotslice
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(iotslice.encode('utf-8') in output)

    def test_returns_iotgateway_create_file_does_not_exist(self):
        name='gateway2'
        cluster='test1'
        iotslice='test1'        
        operation='create'
        configfile='./tests/conf/ghost.toml'
        text= 'Cluster does not exist'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        text= 'Nothing to get'
        operation='get'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_create_cluster_does_not_exist(self):
        name='gateway3'
        cluster='ghost'
        iotslice='test1'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= 'Cluster does not exist'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        text= 'Nothing to get'
        operation='get'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_create_slice_does_not_exist(self):
        name='gateway3'
        cluster='test1'
        iotslice='ghost'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= 'Slice does not exist'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        print(output)
        self.assertTrue(text.encode('utf-8') in output)
        text= 'Nothing to get'
        operation='get'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_attach(self):
        name='test1'
        server='test1'
        operation='attach'
        configfile='./tests/conf/iotorch.toml'
        text= 'Attaching IoT Gateway: ' + name + ' to IoT Server ' + server
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--server='+server, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(server.encode('utf-8') in output)

    def test_returns_iotgateway_attach_gateway_does_not_exist(self):
        name='ghost'
        server='test1'
        operation='attach'
        text='Nothing to update'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--server='+server, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_attach_file_does_not_exist(self):
        name='test'
        server='test1'
        operation='attach'
        text='Nothing to update'
        configfile='./tests/conf/iotorch_not_exist.toml'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--server='+server, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_attach_slice_does_not_exist(self):
        name='test'
        server='ghost'
        operation='attach'
        configfile='./tests/conf/iotorch.toml'
        text= 'IoT Server does not exist'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--server='+server, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_delete(self):
        name='gateway1'
        operation='delete'
        text='Deleting IoT Gateway: ' + name
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        text='Nothing to get'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_delete_gateway_does_not_exist(self):
        name='ghost'
        operation='delete'
        text='Nothing to delete'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_delete_file_does_not_exist(self):
        name='gateway1'
        operation='delete'
        text='Nothing to delete'
        configfile='./tests/conf/iotorch_not_exist.toml'
        output = popen(['iotorch', 'iotgateway', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
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
        configfile='./tests/conf/ghost.toml'
        text='Nothing to list'
        output = popen(['iotorch', 'iotgateway', operation, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

