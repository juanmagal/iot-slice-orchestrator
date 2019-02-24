"""
iotorch iotdevice

  Usage:
    iotorch iotdevice create --name=<name> --gateway=<gateway> [--protocol=<protocol>] [--resource=<resource>]... [--configfile=<name>]   
    iotorch iotdevice [delete|get] --name=<name> [--configfile=<name>]
    iotorch iotdevice list [--configfile=<name>]

"""

from json import dumps

from .base import Base

from docopt import docopt

import toml

import os

from ..utils import k8sutils,gatewayutils

class Iotdevice(Base):
    """The IoT Device command."""

    def create(self):

        config_path = self.options['--configfile']

        if (not config_path):
           config_path='./iotorch.toml'

        devicename = self.options['--name']
        gatewayname = self.options['--gateway']
        resources = self.options['--resource']

        protocol = self.options['--protocol']
 
        # By default we will use SenML format when using MQTT
        # That could be changed in the future
        protocolformat = None
        if protocol == 'MQTT':
           protocolformat = 'SENML'

        deviceparams = {'gateway':gatewayname,'protocol':protocol,'format':protocolformat,'resources':resources}

        device = {devicename:deviceparams}

        config = {}

        devices = device

        if not os.path.exists(config_path):
           print('IoT Gateway does not exist')
           return

        with open(config_path,'r') as f:
           config = toml.load(f)
           f.close
           if config.get('iotdevices') != None:
              devices = config['iotdevices']
              devices.update(device)

        gateways = config.get('iotgateways')

        if gateways == None:
           print('IoT Gateway does not exist')
           return

        gateway = gateways.get(gatewayname)

        if gateway == None:
           print('IoT Gateway does not exist')
           return

        if not gatewayutils.createDevice(gateway.get('gatewayip'),'iotdevice'+devicename,protocol,protocolformat,resources):
           print('Impossible to attach to IoT Gateway')
           return

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

        gatewayname = device.get('gateway')

        gateways = config.get('iotgateways')

        if gateways != None:
           gateway = gateways.get(gatewayname)
           if gateway != None:
              if not gatewayutils.deleteDevice(gateway.get('gatewayip'),'iotdevice'+devicename):
                  print('Impossible to dettach from IoT Gateway')
                  return

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

