"""Tests for our `iotorch slice` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestSlice(TestCase):

    def test_returns_iotslice_create(self):
        output = popen(['iotorch', 'iotslice', 'create'], stdout=PIPE).communicate()[0]
        self.assertTrue('Creating IoT Slice!'.encode('utf-8') in output)

    def test_returns_iotslice_delete(self):
        output = popen(['iotorch', 'iotslice', 'delete'], stdout=PIPE).communicate()[0]
        self.assertTrue('Deleting IoT Slice!'.encode('utf-8') in output)
