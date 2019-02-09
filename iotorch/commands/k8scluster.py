"""
iotorch k8scluster

  Usage:  iotorch k8scluster [create|delete] --name=<name> [--ip=<ipaddress>]   

"""

from json import dumps

from .base import Base

from docopt import docopt

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

    def run(self):

        print(self.options)

        options = docopt(__doc__)

        if options['create']:
            self.options=options
            self.create()
        elif options['delete']:
            self.options=options
            self.delete()
        else:
            print("Option not implemented")    
            raise NotImplementedError('Option not implemented')
