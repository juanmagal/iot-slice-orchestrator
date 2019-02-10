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

    def test_returns_iotdevice_get(self):
        name='test'
        operation='get'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotdevice', operation, '--name='+name, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotdevice_get_file_does_not_exit(self):
        name='test'
        operation='get'
        text='Nothing to get'
        output = popen(['iotorch', 'iotdevice', operation, '--name='+name], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

    def test_returns_iotdevice_list(self):
        name='test'
        operation='list'
        configfile='./tests/conf/iotorch.toml'
        output = popen(['iotorch', 'iotdevice', operation, '--configfile='+configfile], stdout=PIPE).communicate()[0]
        self.assertTrue(name.encode('utf-8') in output)

    def test_returns_iotdevice_list_file_does_not_exist(self):
        name='test'
        operation='list'
        text='Nothing to list'
        output = popen(['iotorch', 'iotdevice', operation], stdout=PIPE).communicate()[0]
        self.assertTrue(text.encode('utf-8') in output)

