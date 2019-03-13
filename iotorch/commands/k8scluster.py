"""
iotorch k8scluster

  Usage:  
    iotorch k8scluster create --name=<name> [--ip=<ipaddress>] [--k8scontext=<context>] [--k8shelmip=<port>]º [--k8shelmport=<port>] [--configfile=<name>]  
    iotorch k8scluster [delete|get] --name=<name> [--configfile=<name>]
    iotorch k8scluster list [--configfile=<name>]

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
      
        clustername = self.options['--name']
        ipaddr=self.options['--ip']
        if ipaddr:
           try:
              ip = ipaddress.ip_address(unicode(ipaddr, "utf-8"))
           except ValueError:
              print('Wrong IP Address format')
              return
        helmport=self.options['--k8shelmport']
        if helmport == None:
           helmport = "44134"
       
        helmip=self.options['--k8shelmport']
        if helmip == None:
           helmip = ipaddr
        else:
           try:
              ip = ipaddress.ip_address(unicode(helmip, "utf-8"))
           except ValueError:
              print('Wrong Helm IP Address format')
              return

        k8s_context = self.options['--k8scontext']

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        clusterparams = {'ip':ipaddr,'k8scontext':k8s_context,'helmport':helmport,'helmip':helmip}

        cluster = {clustername:clusterparams}

        config = {}

        clusters = cluster

        if os.path.exists(config_path):
           with open(config_path,'r') as f:
              config = toml.load(f)
              f.close
              if config.get('k8sclusters') != None:
                 clusters = config['k8sclusters']
                 clusters.update(cluster)

        config.update({'k8sclusters':clusters})
        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('k8s cluster %s created' %clustername)

    def delete(self):

        clustername = self.options['--name']

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

        if config.get('k8sclusters') == None:
           print('Nothing to delete')
           return

        clusters = config.pop('k8sclusters')

        if clusters.get(clustername) == None:
           print('Nothing to delete')
           return

        cluster = clusters.pop(clustername)

        config.update({'k8sclusters:':clusters})

        with open(config_path,'w+') as f:
           toml.dump(config,f)

        print('k8s cluster %s deleted' %clustername)


    def get(self):
        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to get')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               clusters = config.get('k8sclusters')
               if clusters == None:
                   print('Nothing to get')
                   return
               cluster = clusters.get(self.options['--name'])
               if cluster == None:
                   print('Nothing to get')
               else:
                   print(cluster)

    def list(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        if not os.path.exists(config_path):
           print('Nothing to list')
        else:
           with open(config_path) as f:
               config = toml.load(f)
               clusters = config.get('k8sclusters')
               if clusters == None:
                  print('Nothing to list')
               else:
                  print(list(clusters.keys()))

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
