"""
  Usage: iotorch iotserver [create | delete] 

"""

from json import dumps

from .base import Base

from docopt import docopt

class Iotserver(Base):
    """The IoT Server command."""

    def create(self):
        print('Creating IoT Server!')
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

    def delete(self):
        print('Deleting IoT Server!')
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

