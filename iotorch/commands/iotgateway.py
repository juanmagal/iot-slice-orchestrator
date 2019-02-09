"""
iotorch iotgateway

  Usage:  iotorch iotgateway  [create|delete|attach] --name=<name> [--cluster=<cluster>] [--slice=<slice>] [--server=<server>]   

"""

from json import dumps

from .base import Base

from docopt import docopt

class Iotgateway(Base):
    """The IoT Gateway command."""

    def create(self):
        print('Creating IoT Gateway:',self.options['--name'],self.options['--cluster'],self.options['--slice'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

    def delete(self):
        print('Deleting IoT Gateway:',self.options['--name'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

    def attach(self):
        print('Attaching IoT Gateway:',self.options['--name'],'to IoT Server',self.options['--server'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

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
        else:
            print("Option not implemented")
            raise NotImplementedError('Option not implemented')

