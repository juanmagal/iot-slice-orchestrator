"""Tests for our `iotorch IoT Gateway` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestIotGateway(TestCase):

    def test_returns_iotgateway_create(self):
        output = popen(['iotorch', 'iotgateway', 'create'], stdout=PIPE).communicate()[0]
        print (output)
        self.assertTrue('Creating IoT Gateway!'.encode('utf-8') in output)
