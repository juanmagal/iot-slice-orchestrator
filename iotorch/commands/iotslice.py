"""The IoT Slice command."""

from json import dumps

from .base import Base


class Iotslice(Base):
    """The IoT Slice command."""

    def create(self):
        print('Creating IoT Slice!')
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))        

    def run(self):
        if self.options['create']:
            self.create()
        else:
            print("Option not implemented")    
            raise NotImplementedError('Option not implemented')
