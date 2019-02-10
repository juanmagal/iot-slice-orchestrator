"""Tests for our `iotorch slice` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestSlice(TestCase):

    def test_returns_iotslice_create(self):
        name='slice1'
        edge='cluster1'
        server='cluster2'
        operation='create'
        text= 'Creating IoT Slice: ' + name + ' ' + edge + ' ' + server
        output = popen(['iotorch', 'iotslice', operation, '--name='+name, '--edge='+edge,'--cloud='+server], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotslice_delete(self):
        name='slice1'
        operation='delete'
        text='Deleting IoT Slice: ' + name
        output = popen(['iotorch', 'iotslice', operation, '--name='+name], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

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
        output = popen(['iotorch', 'iotslice', operation, '--name='+name], stdout=PIPE).communicate()[0]
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
        text='Nothing to list'
        output = popen(['iotorch', 'iotslice', operation], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

