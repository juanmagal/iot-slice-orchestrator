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
