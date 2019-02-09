"""
iotorch iotslice

  Usage:  iotorch iotslice [create|delete] --name=<name> [--edge=<edgecluster>] [--cloud=<cloudcluster>]    

"""
from json import dumps

from .base import Base

from docopt import docopt

class Iotslice(Base):
    """The IoT Slice command."""

    def create(self):
        print('Creating IoT Slice:',self.options['--name'],self.options['--edge'],self.options['--cloud'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

    def delete(self):
        print('Deleting IoT Slice:',self.options['--name'])
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

    def run(self):

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
