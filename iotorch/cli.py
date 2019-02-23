"""
iotorch

usage: iotorch [--version] [-h | --help] <command> [<args>...]

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  iotorch help
"""

#  iotorch hello
#  iotorch k8scluster create
#  iotorch iotslice create
#  iotorch iotdevice create
#  iotorch iotgateway create
#  iotorch iotserver create
#  iotorch -h | --help
#  iotorch --version

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

from . import utils 

def main():
    """Main CLI entrypoint."""
        
    import iotorch.commands

    options = docopt(__doc__, version=VERSION,options_first=True)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.

    command = options['<command>']

    commandargs = options['<args>']

    try:
       module = getattr(iotorch.commands, command)
    except AttributeError as ae:
       exit(__doc__.split("\n")[3]) 

    iotorch.commands = getmembers(module, isclass)

    commandclass = [commandclass[1] for commandclass in iotorch.commands if commandclass[0] != 'Base'][0] 
    
    commandclass = commandclass(options)

    commandclass.run()

