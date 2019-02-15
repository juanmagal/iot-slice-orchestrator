"""
iotorch iotslice

  Usage:  iotorch iotslice [create|delete|get|list] [--name=<name>] [--edge=<edgecluster>] [--cloud=<cloudcluster>] [--configfile=<name>] 

"""
from json import dumps

from .base import Base

from docopt import docopt

from kubernetes import client, config

import toml

import os

class Iotslice(Base):
    """The IoT Slice command."""

    def create(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        sliceparams = {'edge':self.options['--edge'],'cloud':self.options['--cloud']}

        iotslicename = self.options['--name']

        iotslice = {iotslicename:sliceparams}

        config = {}

        iotslices = iotslice

        if not os.path.exists(config_path):
           print('Clusters do not exist')
           return

        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close
           if config.get('iotslices') != None:
               iotslices = config['iotslices']
               iotslices.update(iotslice)

        clusters = config.get('k8sclusters')
 
        if clusters == None:
           print('Clusters do not exist')
           return

        edge = clusters.get(self.options['--edge'])

        if edge == None:
           print('Edge cluster does not exist')
           return

        cloud = clusters.get(self.options['--cloud'])

        if cloud == None:
           print('Cloud cluster does not exist')
           return

        config.update({'iotslices':iotslices})
        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('IoT Slice %s created' %iotslicename)

    def delete(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to delete')
           return

        iotslicename = self.options['--name']

        config = {}
        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close

        if config.get('iotslices') == None:
           print('Nothing to delete')
           return

        iotslices = config.pop('iotslices')

        if iotslices.get(iotslicename) == None:
           print('Nothing to delete')
           return

        iotslice = iotslices.pop(iotslicename)

        config.update({'iotslices':iotslices})

        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('IoT Slice %s deleted' %iotslicename)

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
