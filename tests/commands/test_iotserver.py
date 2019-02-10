"""Tests for our `iotorch IoT Server` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestIotServer(TestCase):

    def test_returns_iotserver_create(self):
        name='server1'
        cluster='cluster1'
        iotslice='slice1'
        operation='create'
        text= 'Creating IoT Server: ' + name + ' ' + cluster + ' ' + iotslice
        output = popen(['iotorch', 'iotserver', operation, '--name='+name, '--cluster='+cluster,'--slice='+iotslice], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotserver_delete(self):
        name='server1'
        operation='delete'
        text='Deleting IoT Server: ' + name
        output = popen(['iotorch', 'iotserver', operation, '--name='+name], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

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
        output = popen(['iotorch', 'iotserver', operation, '--name='+name], stdout=PIPE).communicate()[0]
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
        output = popen(['iotorch', 'iotserver', operation], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

