"""Tests for our `iotorch slice` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestSlice(TestCase):

    def test_returns_iotslice_create(self):
        output = popen(['iotorch', 'iotslice', 'create'], stdout=PIPE).communicate()[0]
        print (output)
        self.assertTrue('Creating IoT Slice!'.encode('utf-8') in output)
