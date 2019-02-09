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
