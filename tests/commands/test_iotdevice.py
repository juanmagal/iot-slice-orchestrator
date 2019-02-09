"""Tests for our `iotorch IoT Device` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestIoTDevice(TestCase):

    def test_returns_iotdevice_create(self):
        name='device1'
        operation='create'
        text= 'Creating IoT Device: ' + name
        output = popen(['iotorch', 'iotdevice', operation, '--name='+name], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)


    def test_returns_iotdevice_delete(self):
        name='device1'
        operation='delete'
        text='Deleting IoT Device: ' + name
        output = popen(['iotorch', 'iotdevice', operation, '--name='+name], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

