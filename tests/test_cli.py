"""Tests for our main iotorch CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from iotorch import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['iotorch', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('usage:'.encode('utf-8') in output)

        output = popen(['iotorch', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('usage:'.encode('utf8') in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['iotorch', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), VERSION.encode('utf-8'))
