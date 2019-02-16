"""
iotorch iotdevice

  Usage:
    iotorch iotdevice create --name=<name> --gateway=<gateway> [--configfile=<name>]   
    iotorch iotdevice [delete|get] --name=<name> [--configfile=<name>]
    iotorch iotdevice list [--configfile=<name>]

"""

from json import dumps

from .base import Base

from docopt import docopt

import toml

import os

class Iotdevice(Base):
    """The IoT Device command."""

    def create(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        devicename = self.options['--name']

        deviceparams = {'gateway':self.options['--gateway']}

        device = {devicename:deviceparams}

        config = {}

        devices = device

        if os.path.exists(config_path):
           with open(config_path,'r') as f:
              config = toml.load(f)
              devices = config['iotdevices']
              devices.update(device)
              f.close
       
        config.update({'iotdevices':devices})
        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print("IoT Device %s created" %devicename)

    def delete(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to delete')
           return

        devicename = self.options['--name']

        config = {}
        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close

        if config.get('iotdevices') == None:
           print('Nothing to delete')
           return
	  
        devices = config.pop('iotdevices')

        if devices.get(devicename) == None:
           print('Nothing to delete')
           return

        device = devices.pop(devicename)

        config.update({'iotdevices':devices})

        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print("IoT Device %s deleted" %devicename)


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

