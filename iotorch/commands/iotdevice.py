"""
iotorch iotdevice

  Usage:  iotorch iotdevice [create|delete|get|list] [--name=<name>] [--configfile=<name>]   

"""

from json import dumps

from .base import Base

from docopt import docopt

import toml

import os

class Iotdevice(Base):
    """The IoT Device command."""

    def create(self):
        print('Creating IoT Device:',self.options['--name'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))        

    def delete(self):
        print('Deleting IoT Device:',self.options['--name'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

    def get(self):
        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to get')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               devices = config['iotdevice']
               print(devices[self.options['--name']])

    def list(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to list')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               devices = config['iotdevice']
               print (list(devices.keys()))

    def run(self):

        options = docopt(__doc__)

        if options['create']:
            self.options=options
            self.create()
        elif options['delete']:
            self.options=options
            self.delete()
        elif options['get']:
            self.options=options
            self.get()
        elif options['list']:
            self.options=options
            self.list()
        else:
            print("Option not implemented")
            raise NotImplementedError('Option not implemented')

