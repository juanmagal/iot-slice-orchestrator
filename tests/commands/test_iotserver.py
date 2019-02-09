"""Tests for our `iotorch IoT Server` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestIotServer(TestCase):

    def test_returns_iotserver_create(self):
        output = popen(['iotorch', 'iotserver', 'create'], stdout=PIPE).communicate()[0]
        self.assertTrue('Creating IoT Server!'.encode('utf-8') in output)

    def test_returns_iotserver_delete(self):
        output = popen(['iotorch', 'iotserver', 'delete'], stdout=PIPE).communicate()[0]
        self.assertTrue('Deleting IoT Server!'.encode('utf-8') in output)
