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

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        gatewayparams = {'cluster':self.options['--cluster'],'slice':self.options['--slice']}

        gateway = {self.options['--name']:gatewayparams}

        config = {}

        gateways = gateway

        if os.path.exists(config_path):
           with open(config_path,'r') as f:
              config = toml.load(f)
              f.close
              if config.get('iotgateways') != None:
                 gateways = config['iotgateways']
                 gateways.update(gateway)

        config.update({'iotgateways':gateways})
        with open(config_path,'w+') as f:
           toml.dump(config,f)

    def delete(self):

        print('Deleting IoT Gateway:',self.options['--name'])
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

        if config.get('iotgateways') == None:
           print('Nothing to delete')
           return

        gateways = config.pop('iotgateways')

        if gateways.get(self.options['--name']) == None:
           print('Nothing to delete')
           return

        gateway = gateways.pop(self.options['--name'])

        config.update({'iotgateways':gateways})

        with open(config_path,'w+') as f:
           toml.dump(config,f)


    def attach(self):
        print('Attaching IoT Gateway:',self.options['--name'],'to IoT Server',self.options['--server'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to update')
           return

        config = {}
        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close

        if config.get('iotgateways') == None:
           print('Nothing to update')
           return

        gateways = config.pop('iotgateways')
        
        if gateways.get(self.options['--name']) == None:
           print('Nothing to update')
           return

        gateway = gateways.pop(self.options['--name'])

        if gateway == None:
           print('Nothing to update')
           return

        gateway['server'] = self.options['--server']
  
        gateway = {self.options['--name']:gateway}
 
        gateways.update(gateway)

        config.update({'iotgateways':gateways})

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
               gateways = config.get('iotgateways')
               if gateways == None:
                   print('Nothing to get')
                   return
               gateway = gateways.get(self.options['--name'])
               if gateway == None:
                   print('Nothing to get')
               else:
                   print(gateway)

    def list(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to list')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               gateways = config.get('iotgateways')
               if gateways == None:
                  print('Nothing to list')
               else:
                  print (list(gateways.keys()))


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

