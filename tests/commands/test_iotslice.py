"""Tests for our `iotorch slice` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestSlice(TestCase):

    def test_returns_iotslice_get(self):
        name='test'
        operation='get'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotslice_get_file_does_not_exit(self):
        name='test'
        operation='get'
        text='Nothing to get'
        configfile='./tests/conf/iotorch_not_exist.toml'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotslice_create(self):
        name='slice1'
        edge='test1'
        server='test1'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= "IoT Slice " + name + " created"
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--edge='+edge,'--cloud='+server, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(edge.encode('utf-8') in output)

    def test_returns_iotslice_create_file_does_not_exist(self):
        name='slice2'
        edge='test1'
        server='test1'
        operation='create'
        configfile='./tests/conf/ghost.toml'
        text= 'Clusters do not exist'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--edge='+edge,'--cloud='+server, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        text= 'Nothing to get'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotslice_create_edge_cluster_does_not_exist(self):
        name='slice3'
        edge='ghost'
        server='test1'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= 'Edge cluster does not exist'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--edge='+edge,'--cloud='+server, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        text= 'Nothing to get'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        print(output)
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotslice_create_cloud_cluster_does_not_exist(self):
        name='slice4'
        edge='test1'
        server='ghost'
        operation='create'
        configfile='./tests/conf/iotorch.toml'
        text= 'Cloud cluster does not exist'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--edge='+edge,'--cloud='+server, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        text= 'Nothing to get'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        print(output)
        self.assertTrue(text.encode('utf-8') in output)


    def test_returns_iotslice_delete(self):
        name='test1'
        operation='delete'
        text= "IoT Slice " + name + " deleted"        
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)
        operation='get'
        text='Nothing to get'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotslice_delete_device_does_not_exist(self):
        name='ghost'
        operation='delete'
        text='Nothing to delete'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotslice_delete_file_does_not_exist(self):
        name='server1'
        operation='delete'
        text='Nothing to delete'
        configfile='./tests/conf/iotorch_not_exist.toml'
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotslice_list(self):
        name='test'
        operation='list'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotslice', operation, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotslice_list_file_does_not_exist(self):
        name='test'
        operation='list'
        configfile='./tests/conf/iotorch_not_exist.toml'
        text='Nothing to list'
        output = popen(['iotorch', 'iotslice', operation, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

