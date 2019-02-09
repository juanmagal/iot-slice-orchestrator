"""
  usage: iotorch hello

"""

from docopt import docopt

from json import dumps

from .base import Base


class Hello(Base):
    """Say hello, world!"""

    def run(self):

        options = docopt(__doc__)
        
        print('Hello, world!')
        print('You supplied the following options:', dumps(options, indent=2, sort_keys=True))
