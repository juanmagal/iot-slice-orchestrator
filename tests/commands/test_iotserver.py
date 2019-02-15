"""Tests for our `iotorch IoT Server` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestIotServer(TestCase):

    def test_returns_iotserver_get(self):
        name='test'
        operation='get'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotserver_get_file_does_not_exit(self):
        name='test'
        operation='get'
        text='Nothing to get'
        configfile='./tests/conf/iotorch_not_exist.toml'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotserver_create(self):
        name='server1'
        cluster='test1'
        iotslice='test1'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= "IoT Server " + name + " created"
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice,'--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(cluster.encode('utf-8') in output)

    def test_returns_iotserver_create_file_does_not_exist(self):
        name='server2'
        cluster='test1'
        iotslice='test1'
        operation='create'
        configfile='./tests/conf/iotorch_test.toml'
        text= 'Cluster does not exist'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice,'--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        text= 'Nothing to get'
        operation='get'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotserver_create_cluster_does_not_exist(self):
        name='server3'
        cluster='ghost'
        iotslice='test1'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= 'Cluster does not exist'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice,'--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        text= 'Nothing to get'
        operation='get'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotgateway_create_slice_does_not_exist(self):
        name='gateway3'
        cluster='test1'
        iotslice='ghost'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= 'Slice does not exist'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice,'--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        text= 'Nothing to get'
        operation='get'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotserver_delete(self):
        name='server1'
        operation='delete'
        text= "IoT Server " + name + " deleted"
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        text='Nothing to get'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotserver_delete_device_does_not_exist(self):
        name='ghost'
        operation='delete'
        text='Nothing to delete'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotserver_delete_file_does_not_exist(self):
        name='server1'
        operation='delete'
        text='Nothing to delete'
        configfile='./tests/conf/iotorch_not_exist.toml'
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotserver_list(self):
        name='test'
        operation='list'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotserver', operation, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotserver_list_file_does_not_exist(self):
        name='test'
        operation='list'
        text='Nothing to list'
        configfile='./tests/conf/iotorch_not_exist.toml'
        output = popen(['iotorch', 'iotserver', operation, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

