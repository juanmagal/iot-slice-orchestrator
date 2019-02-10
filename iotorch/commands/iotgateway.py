"""
iotorch iotgateway

  Usage:  iotorch iotgateway  [create|delete|attach|get|list] [--name=<name>] [--cluster=<cluster>] [--slice=<slice>] [--server=<server>] [--configfile=<name>]  

"""

from json import dumps

from .base import Base

from docopt import docopt

import toml

import os

class Iotgateway(Base):
    """The IoT Gateway command."""

    def create(self):
        print('Creating IoT Gateway:',self.options['--name'],self.options['--cluster'],self.options['--slice'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

    def delete(self):
        print('Deleting IoT Gateway:',self.options['--name'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

    def attach(self):
        print('Attaching IoT Gateway:',self.options['--name'],'to IoT Server',self.options['--server'])
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
               devices = config['iotgateway']
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
               devices = config['iotgateway']
               print (list(devices.keys()))



    def run(self):

        options = docopt(__doc__)

        if options['create']:
            self.options=options
            self.create()
        elif options['delete']:
            self.options=options
            self.delete()
        elif options['attach']:
            self.options=options
            self.attach()
        elif options['get']:
            self.options=options
            self.get()
        elif options['list']:
            self.options=options
            self.list()
        else:
            print("Option not implemented")
            raise NotImplementedError('Option not implemented')

