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

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        gatewayname = self.options['--name']

        gatewayparams = {'cluster':self.options['--cluster'],'slice':self.options['--slice']}

        gateway = {gatewayname:gatewayparams}

        config = {}

        gateways = gateway

        if not os.path.exists(config_path):
           print('Cluster does not exist')
           return

        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close
           if config.get('iotgateways') != None:
              gateways = config['iotgateways']
              gateways.update(gateway)

        clusters = config.get('k8sclusters')

        if clusters == None:
           print('Cluster does not exist')
           return

        cluster = clusters.get(self.options['--cluster'])

        if cluster == None:
           print('Cluster does not exist')
           return

        iotslices = config.get('iotslices')

        if iotslices == None:
           print('Slice does not exist')
           return

        iotslice = iotslices.get(self.options['--slice'])

        if iotslice == None:
           print('Slice does not exist')
           return

        config.update({'iotgateways':gateways})
        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('IoT Gateway %s created' %gatewayname)


    def delete(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to delete')
           return

        config = {}

        gatewayname = self.options['--name']

        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close

        if config.get('iotgateways') == None:
           print('Nothing to delete')
           return

        gateways = config.pop('iotgateways')

        if gateways.get(gatewayname) == None:
           print('Nothing to delete')
           return

        gateway = gateways.pop(gatewayname)

        config.update({'iotgateways':gateways})

        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('IoT Gateway %s deleted' %gatewayname)

    def attach(self):

        config_path = self.options['--configfile']

        gatewayname = self.options['--name']
        servername = self.options['--server']

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
        
        if gateways.get(gatewayname) == None:
           print('Nothing to update')
           return

        gateway = gateways.pop(gatewayname)

        if gateway == None:
           print('Nothing to update')
           return

        servers = config.get('iotservers')

        if servers == None:
           print('IoT Server does not exist')
           return

        server = servers.get(servername)

        if server == None:
           print('IoT Server does not exist')
           return

        gateway['server'] = servername
  
        gateway = {gatewayname:gateway}
 
        gateways.update(gateway)

        config.update({'iotgateways':gateways})

        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('IoT Gateway %s attached to IoT Server %s' %(gatewayname,servername))

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

