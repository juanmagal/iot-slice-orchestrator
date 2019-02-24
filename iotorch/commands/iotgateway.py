"""
iotorch iotgateway

  Usage:  
    iotorch iotgateway  create --name=<name> --cluster=<cluster> --slice=<slice> [--helmpath=<path>] [--configfile=<name>]
    iotorch iotgateway  attach --name=<name> --server=<server> [--configfile=<name>]
    iotorch iotgateway  [delete|get] --name=<name> [--configfile=<name>]
    iotorch iotgateway  list [--configfile=<name>]

"""

from json import dumps

from .base import Base

from docopt import docopt

import toml

import os

from ..utils import k8sutils,serverutils,gatewayutils

class Iotgateway(Base):
    """The IoT Gateway command."""

    def create(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        helm_path = self.options['--helmpath']

        gatewayname = self.options['--name']

        clustername = self.options['--cluster']

        slicename = self.options['--slice']

        gatewayparams = {'cluster':clustername,'slice':slicename,'helmpath':helm_path}

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

        cluster = clusters.get(clustername)

        if cluster == None:
           print('Cluster does not exist')
           return

        iotslices = config.get('iotslices')

        if iotslices == None:
           print('Slice does not exist')
           return

        iotslice = iotslices.get(slicename)

        if iotslice == None:
           print('Slice does not exist')
           return

        if not k8sutils.createiotgatewayincluster(slicename,clustername,helm_path,config_path):
           print('IoT Gateway not deployed in cluster %s' %cluster)
           return

        gatewayip =  k8sutils.getgatewayip(slicename,clustername,config_path)

        if gatewayip == None:
           print('IoT Gateway not sucessfully deployed in cluster %s' %cluster)
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

        slicename = gateway.get('slice')
        clustername = gateway.get('cluster')
        servername = gateway.get('server')

        # Check if gateway was attached
        if servername != None:
           servers = config.get('iotservers')
           if servers != None:
              server = servers.get(servername)
              if server != None:
                 if not serverutils.deleteDevice(server.get('serverip'),gateway.get('servertopicuser'),server.get('username'),server.get('password')):
                    print('IoT Gateway not dettached from IoT Server %s' %servername)
                    return
                 else:
                    gatewayexporterip =  k8sutils.getexportergatewayip(slicename,clustername,config_path)
                    if not gatewayutils.deleteExporter(gatewayexporterip,gatewayname):
                       print('IoT Gateway not dettached from IoT Server %s' %servername)
                       return

        if not k8sutils.deleteiotgatewayincluster(slicename,clustername,config_path):
           print('IoT Gateway not removed from cluster %s' %cluster)
           return

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

        response = serverutils.createDevice(server.get('serverip'),'iotgateway-'+gatewayname,server.get('username'),server.get('password'))

        if response == None:
           print('Impossible to attach to IoT Server')
           return

        slicename = gateway.get('slice')
        clustername = gateway.get('cluster')

        gatewayexporterip =  k8sutils.getexportergatewayip(slicename,clustername,config_path)

        if gatewayexporterip == None:
           print('IoT Gateway could not be updated')
           return

        gateway['server'] = servername
        gateway['servertopicuser'] = response['device']
        gateway['servertopicpassword'] = response['key']
        gateway['servertopic'] = 'channels/'+response['channel']+'/messages'
        gateway['exporterip'] = gatewayexporterip

        if not gatewayutils.createExporter(gatewayexporterip,gatewayname,servername,server.get('serverip'),gateway.get('servertopic'),gateway.get('servertopicuser'),gateway.get('servertopicpassword')):
           print('IoT Gateway could not be updated')
           return

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

