"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from iotorch import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        print("run tests")
        errno = call(['py.test', '--cov=iotorch', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'iotorch',
    version = __version__,
    description = 'A CLI for creating IoT Slices implemented in Python.',
    long_description = long_description,
    url = 'https://github.com/juanmagal/iot-slice-orchestrator',
    author = 'Juan Manuel Fernandez',
    author_email = 'juanma.galmes@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: IoT',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt','toml','kubernetes','pyhelm'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'iotorch=iotorch.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
