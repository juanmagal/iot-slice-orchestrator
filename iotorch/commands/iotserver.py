"""
iotorch iotserver

  Usage: 
    iotorch iotserver create --name=<name> --cluster=<cluster> --slice=<slice> [--helmpath=<path>] [--configfile=<name>] 
    iotorch iotserver set --name=<name> --user=<username> --password=<password> [--configfile=<name>]
    iotorch iotserver [delete | get] --name=<name> [--configfile=<name>]
    iotorch iotserver list [--configfile=<name>]

"""
from json import dumps

from .base import Base

from docopt import docopt

import toml

import os

from ..utils import k8sutils,serverutils

class Iotserver(Base):
    """The IoT Server command."""

    def create(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'
  
        servername = self.options['--name']

        slicename = self.options['--slice']

        clustername = self.options['--cluster']

        helm_path = self.options['--helmpath']

        serverparams = {'cluster':clustername,'slice':slicename, 'helmpath':helm_path}

        server = {servername:serverparams}

        config = {}

        servers = server

        if not os.path.exists(config_path):
           print('Cluster does not exist')
           return

        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close
           if config.get('iotservers') != None:
               servers = config.get('iotservers') 
               servers.update(server)

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

        if not k8sutils.createiotserverincluster(slicename,clustername,helm_path,config_path):
           print('IoT Server not deployed in cluster %s' %cluster)
           return

        config.update({'iotservers':servers})
        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('IoT Server %s created' %servername)

    def set(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        servername = self.options['--name']

        username = self.options['--user']

        password = self.options['--password']

        serverparams = {'username':username,'password':password}

        config = {}

        if not os.path.exists(config_path):
           print('Nothing to set')
           return

        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close
           if config.get('iotservers') == None:
               print('Nothing to set')
               return

        servers = config.get('iotservers')

        server = servers.get(servername)

        if server == None:
           print('Nothing to delete')
           return

        server.update(serverparams)

        servers.update(server)

        # Create user in mainflux

        clustername = server.get('cluster')
        slicename = server.get('slice')

        serverip = k8sutils.getserverip(slicename,clustername,config_path)

        if not serverip:
           print('IoT Server %s not found' %servername)
           return

        if not serverutils.createServerUser(username, password, clustername, serverip):
           print('User was not created in IoT Server %s' %servername)
           return

        servers.update({servername:{'serverip':serverip}})

        config.update({'iotservers':servers})

        with open(config_path,'w+') as f:
           toml.dump(config,f)
      
        print('IoT Server %s set' %servername)

    def delete(self):

        config_path = self.options['--configfile']

        servername = self.options['--name']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to delete')
           return

        config = {}
        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close

        if config.get('iotservers') == None:
           print('Nothing to delete')
           return

        servers = config.pop('iotservers')

        if servers.get(servername) == None:
           print('Nothing to delete')
           return

        server = servers.pop(servername)

        slicename = server.get('slice')

        if slicename == None:
           print('No slice is assigned to this IoT Server')
           return

        clustername = server.get('cluster')

        if clustername == None:
           print('No cluster is assigned to this IoT Server')
           return

        if not k8sutils.deleteiotserverincluster(slicename,clustername,config_path):
           print('IoT Server not removed from cluster %s' %cluster)
           return

        config.update({'iotservers':servers})

        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('IoT Server %s deleted' %servername)

    def get(self):
        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to get')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               servers = config.get('iotservers')
               if servers == None:
                   print('Nothing to get')
                   return
               server = servers.get(self.options['--name'])
               if server == None:
                   print('Nothing to get')
               else:
                   print(server)

    def list(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to list')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               servers = config.get('iotservers')
               if servers == None:
                  print('Nothing to list')
               else:
                  print (list(servers.keys()))


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
        elif options['set']:
            self.options=options
            self.set()
        else:
            print("Option not implemented")
            raise NotImplementedError('Option not implemented')

