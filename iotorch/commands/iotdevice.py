"""
iotorch iotdevice

  Usage:  iotorch iotdevice [create|delete|get|list] [--name=<name>] [--gateway=<gateway>] [--configfile=<name>]   

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

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        iotgateway = {'gateway':self.options['--gateway']}

        device = {self.options['--name']:iotgateway}

        config = {}

        devices = device

        if os.path.exists(config_path):
           with open(config_path,'r') as f:
              config = toml.load(f)
              print(config)
              devices = config['iotdevices']
              print(devices)
              devices.update(device)
              print(devices)
              f.close
       
        config.update({'iotdevices':devices})
        print(config)
        with open(config_path,'w+') as f:
           toml.dump(config,f)

    def delete(self):
        print('Deleting IoT Device:',self.options['--name'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to delete')
           return

        config = {}
        with open(config_path,'r') as f:
           config = toml.load(f)
           print(config)
           f.close

        devices = config.pop('iotdevices')
        print(devices)
        device = devices.pop(self.options['--name'])
        config.update({'iotdevices':devices})
        print(devices)

        config.update({'iotdevices':devices})
        print(config)
        with open(config_path,'w+') as f:
           toml.dump(config,f)



    def get(self):
        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to get')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               devices = config.get('iotdevices')
               device = devices.get(self.options['--name'])
               if device == None:
                   print('Nothing to get')
               else:
                   print(device)

    def list(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to list')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               devices = config.get('iotdevices')
               if devices == None:
                  print('Nothing to list')
               else:
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

