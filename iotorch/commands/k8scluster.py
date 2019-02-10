"""
iotorch k8scluster

  Usage:  iotorch k8scluster [create|delete|get|list] [--name=<name>] [--ip=<ipaddress>] [--configfile=<name>]  

"""
from json import dumps

from .base import Base

from docopt import docopt

import toml

import os

import ipaddress

class K8scluster(Base):
    """The k8s cluster command."""

    def create(self):
        ipaddr=self.options['--ip']
        if ipaddr:
           try:
              ip = ipaddress.ip_address(ipaddr)
           except ValueError:
              print('Wrong IP Address format')
              return
        
        print('Creating k8s cluster:',self.options['--name'],self.options['--ip'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))        

    def delete(self):
        print('Deleting k8s cluster:',self.options['--name'])
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
               clusters = config['k8scluster']
               print(clusters[self.options['--name']])

    def list(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to list')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               clusters = config['k8scluster']
               print (list(clusters.keys()))



    def run(self):

        print(self.options)

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
