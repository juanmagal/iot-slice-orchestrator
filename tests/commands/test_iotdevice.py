"""Tests for our `iotorch IoT Device` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestIoTDevice(TestCase):

    def test_returns_iotdevice_create(self):
        output = popen(['iotorch', 'iotdevice', 'create'], stdout=PIPE).communicate()[0]
        print (output)
        self.assertTrue('Creating IoT Device!'.encode('utf-8') in output)
