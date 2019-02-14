"""
iotorch iotslice

  Usage:  iotorch iotslice [create|delete|get|list] [--name=<name>] [--edge=<edgecluster>] [--cloud=<cloudcluster>] [--configfile=<name>] 

"""
from json import dumps

from .base import Base

from docopt import docopt

import toml

import os

class Iotslice(Base):
    """The IoT Slice command."""

    def create(self):
        print('Creating IoT Slice:',self.options['--name'],self.options['--edge'],self.options['--cloud'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        sliceparams = {'edge':self.options['--edge'],'cloud':self.options['--cloud']}

        iotslice = {self.options['--name']:sliceparams}

        config = {}

        iotslices = iotslice

        if os.path.exists(config_path):
           with open(config_path,'r') as f:
              config = toml.load(f)
              f.close
              if config.get('iotslices') != None:
                  iotslices = config['iotslices']
                  iotslices.update(iotslice)

        config.update({'iotslices':iotslices})
        with open(config_path,'w+') as f:
           toml.dump(config,f)

    def delete(self):

        print('Deleting IoT Slice:',self.options['--name'])
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
           f.close

        if config.get('iotslices') == None:
           print('Nothing to delete')
           return

        iotslices = config.pop('iotslices')

        if iotslices.get(self.options['--name']) == None:
           print('Nothing to delete')
           return

        iotslice = iotslices.pop(self.options['--name'])

        config.update({'iotslices':iotslices})

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
               slices = config.get('iotslices')
               if slices == None:
                  print('Nothing to get')
                  return
               iotslice = slices.get(self.options['--name'])
               if iotslice == None:
                   print('Nothing to get')
               else:
                   print(iotslice)

    def list(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to list')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               slices = config.get('iotslices')
               if slices == None:
                  print('Nothing to list')
               else:
                  print (list(slices.keys()))


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
