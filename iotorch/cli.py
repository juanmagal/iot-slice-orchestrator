"""
iotorch

Usage:
  iotorch hello
  iotorch -h | --help
  iotorch --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  iotorch help
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import iotorch.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(iotorch.commands, k) and v:
            module = getattr(iotorch.commands, k)
            iotorch.commands = getmembers(module, isclass)
            command = [command[1] for command in iotorch.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
